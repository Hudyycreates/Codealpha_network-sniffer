# Network Sniffer 🔍

A Python-based network sniffer built on a Linux VM that captures live packets and analyzes their content, protocols, ports and headers.

## What it does

- Captures live network packets in real time
- Displays source and destination IP addresses
- Identifies protocols — TCP, UDP and ICMP
- Shows port numbers for TCP and UDP traffic
- Reads and displays packet payload data

## Requirements

- Linux (tested on Ubuntu VM)
- Python 3
- Scapy

```bash
sudo apt install python3-scapy
```

## How to run

```bash
sudo python3 sniffer.py
```

Root is required to access raw network packets.

## Example output

```
packet: 10.0.2.15 --> 142.250.74.46 [TCP] 54321 --> 80
packet: 10.0.2.15 --> 8.8.8.8 [UDP] 12345 --> 53
packet: 10.0.2.15 --> 1.1.1.1 [ICMP]
```

## What I learned

- How packets are structured in layers — Ethernet, IP, TCP/UDP and payload
- How to read and analyze packet information to spot unusual activity
- Watched a real TCP 3-way handshake between my VM and an external server
- How protocols like ARP, DNS and NTP work in the background even when idle
- How to create and edit Python files directly in Linux using nano
- How to connect a Linux VM to GitHub and push code using Git

## What I would add next

- A summary section at the end showing total packets captured, most common IPs and protocol breakdown

## Tools used

- Python 3
- Scapy
- Linux VM (VirtualBox)
- Git / GitHub
