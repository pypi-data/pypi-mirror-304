# -*- coding: utf-8 -*-
# from scapy.all import *
# 将一个pcap包分成若干个pcap包
# 为了解决大pcap分隔慢的问题，使用hash + dic进行辅助定位

import os
import dpkt
from dpkt.utils import inet_to_str
import json
from datetime import datetime
import warnings
import scapy.all as scapy

# 获取当前时间
now = datetime.now()


datalink = 1


def get_packet_lengths(packet_bytes):
    """
    从bytes类型的数据包中获取有效负载长度（减去IP头部和TCP/UDP头部）。

    参数:
    packet_bytes -- 字节串，表示网络数据包

    返回:
    payload_length -- 有效负载长度（字节）
    """
    # 检查字节串是否足够长以包含以太网和IP头部
    # 确保IP头部存在（至少20字节）
    ETHERNET_HEADER_LENGTH = 14
    IP_HEADER_MIN_LENGTH = 20
    if len(packet_bytes) < 20:
        warnings.warn(
            "数据包太短，无法包含完整的IP头部。", category=Warning, source=None
        )
        return None, None

    ip_header_start = ETHERNET_HEADER_LENGTH

    # 获取IP头部的长度（第一个字节的低四位表示头部长度，以4字节为单位）
    ip_header_length = (packet_bytes[ip_header_start] & 0x0F) * 4

    # 检查IP头部长度是否有效
    if ip_header_length < IP_HEADER_MIN_LENGTH:
        warnings.warn("IP头部长度无效。", category=Warning, source=None)
        return None, None

    # IP数据包长度（第16和17个字节，IP头部的第二个字段）
    ip_length_bytes = packet_bytes[
        ETHERNET_HEADER_LENGTH + 2 : ETHERNET_HEADER_LENGTH + 4
    ]

    ip_length = int.from_bytes(ip_length_bytes, byteorder="big")
    # IP协议类型（第10个字节）
    protocol = packet_bytes[ip_header_start + 9]

    # TCP头部或UDP头部的起始位置
    transport_header_start = ip_header_start + ip_header_length

    if protocol == 6:  # TCP
        # TCP头部长度（第12个字节的高4位，以4字节为单位）
        tcp_header_length = (packet_bytes[transport_header_start + 12] >> 4) * 4
        payload_length = ip_length - ip_header_length - tcp_header_length

    elif protocol == 17:  # UDP
        # UDP头部长度固定为8字节
        udp_header_length = 8
        payload_length = ip_length - ip_header_length - udp_header_length

    else:
        warnings.warn("不支持的协议类型。", category=Warning, source=None)
        return None, None

    return payload_length


def getIP(datalink, pkt):
    IP = False
    if datalink == 1 or datalink == 239:  # ethernet frame
        IP = dpkt.ethernet.Ethernet(pkt).data
    # 是RAW_IP包，没有Ethernet层:
    elif datalink == 228 or datalink == 229 or datalink == 101:
        IP = dpkt.ip.IP(pkt)
        # dpkt.ip6.IP6
    else:
        raise TypeError("Unrecognized link-layer protocol!!!!")
    return IP


def get_payload_size(ip, pro_txt):
    ip_header_length = ip.hl * 4
    ip_total_length = ip.len
    if pro_txt == "TCP":
        transport_header_length = ip.data.off * 4
    elif pro_txt == "UDP":
        transport_header_length = 8  # UDP头部长度固定为8字节
    else:
        return None

    payload_size = ip_total_length - ip_header_length - transport_header_length
    return payload_size


def process_pcap_file(file_name, tcp_from_first_packet):
    tcpstream = {}
    f = open(file_name, "rb")
    try:
        pkts = dpkt.pcap.Reader(f)
    except ValueError:
        f.close()
        f = open(file_name, "rb")
        pkts = dpkt.pcapng.Reader(f)
    except Exception as e:
        f.close()
        raise TypeError(f"Unable to open the pcap file: {e}")
    global datalink
    datalink = pkts.datalink()
    number = -1
    try:
        for time, pkt in pkts:
            number += 1
            ip = getIP(datalink, pkt)
            if not isinstance(ip, dpkt.ip.IP):
                warnings.warn(
                    "this packet is not ip packet, ignore.",
                    category=Warning,
                    source=None,
                )
                continue
            if isinstance(ip.data, dpkt.udp.UDP):
                pro_txt = "UDP"
            elif isinstance(ip.data, dpkt.tcp.TCP):
                pro_txt = "TCP"
            else:
                continue
            pro = ip.data
            payload = get_payload_size(ip, pro_txt)
            # if payload is None:
            # continue

            srcport = pro.sport
            dstport = pro.dport
            srcip = inet_to_str(ip.src)
            dstip = inet_to_str(ip.dst)
            siyuanzu1 = (
                srcip
                + "_"
                + str(srcport)
                + "_"
                + dstip
                + "_"
                + str(dstport)
                + "_"
                + pro_txt
            )
            siyuanzu2 = (
                dstip
                + "_"
                + str(dstport)
                + "_"
                + srcip
                + "_"
                + str(srcport)
                + "_"
                + pro_txt
            )
            if siyuanzu1 in tcpstream:
                tcpstream[siyuanzu1].append([time, f"+{payload}", number])
            elif siyuanzu2 in tcpstream:
                tcpstream[siyuanzu2].append([time, f"-{payload}", number])
            else:
                if pro_txt == "TCP":
                    first_flag = getIP(datalink, pkt).data.flags
                    if first_flag != 2 and tcp_from_first_packet:
                        continue
                tcpstream[siyuanzu1] = []
                tcpstream[siyuanzu1].append([time, f"+{payload}", number])

    except dpkt.dpkt.NeedData:
        # logger.info(f"{file_name}PCAP capture is truncated, stopping processing...")
        pass
    f.close()
    return tcpstream


def save_to_json(tcpstream, input_pcap_file, dir):
    # 处理每个表格
    tcpstreams = []
    for stream in tcpstream:
        # 分离数据到两个列表
        time_stamps = [item[0] for item in tcpstream[stream]]
        lengths = [item[1] for item in tcpstream[stream]]

        # 创建包含两个键的字典
        dict = {"timestamp": time_stamps, "payload": lengths}
        (
            dict["src_ip"],
            dict["src_port"],
            dict["dst_ip"],
            dict["dst_port"],
            dict["protocol"],
        ) = stream.split("_")

        tcpstreams.append(dict)

    # 将所有表格转换为 JSON 格式的字符串
    json_lines = [json.dumps(stream, separators=(",", ":")) for stream in tcpstreams]
    json_data = "[\n" + ",\n".join(json_lines) + "\n]"

    # 将 JSON 字符串写入文件
    output_path = os.path.join(dir, f"{os.path.basename(input_pcap_file)}.json")
    with open(output_path, "w") as json_file:
        json_file.write(json_data)

    return True


def save_to_pcap(tcpstream, input_pcap_file, output_dir):
    packets = scapy.rdpcap(input_pcap_file)
    for stream in tcpstream:
        pcap_name = f"{os.path.basename(input_pcap_file)}_{stream}.pcap"
        output_path = os.path.join(output_dir, pcap_name)
        scapy.wrpcap(output_path, [])
        for packet in tcpstream[stream]:
            scapy.wrpcap(output_path, [packets[packet[2]]], append=True)
    return True


def split_flow(
    input_pcap_file, output_dir, tcp_from_first_packet=False, output_type="pcap"
):
    """
    input_pcap_file：需要分隔的pcap包或者pcapng包
    output_dir：文件保存路径
    tcp_from_first_packet：TCP协议是否从第一个连接包开始分隔
    output_type：输出文件的类型（pcap, json）
    """
    if output_type != "pcap" and output_type != "json":
        raise OSError("output type is error! please select pcap or json")
    tcpstream = process_pcap_file(input_pcap_file, tcp_from_first_packet)
    os.makedirs(output_dir, exist_ok=True)
    # 将当前时间格式化为所需的字符串形式
    if output_type == "pcap":
        return save_to_pcap(tcpstream, input_pcap_file, output_dir)
    elif output_type == "json":
        return save_to_json(tcpstream, input_pcap_file, output_dir)
