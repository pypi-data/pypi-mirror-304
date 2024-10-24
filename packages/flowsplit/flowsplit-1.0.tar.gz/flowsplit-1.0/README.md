# flowsplit介绍

flowsplit 是一个用于分隔pcap网络流量的 Python 库，将流量按照session进行分隔，可以输出pcap格式和json格式。

## 安装

```bash
pip install flowsplit
```

## Quick Start

```python
from flowsplit import split_flow

origin_pcap = "/path/dir/filename"
output_dir = "/path/dir/output_dir"

# 分流之后以pcap格式输出，TCP流允许从中途开始（即没有握手过程）
split_flow(origin_pcap, output_dir, tcp_from_first_packet=False, output_type="pcap")

# 分流之后以json格式输出，输出一个json文件，其中每一个单元表示一条流，TCP流必须从握手阶段开始，从中途开始的TCP流会被丢弃
split_flow(origin_pcap, output_dir, tcp_from_first_packet=True, output_type="json")
```