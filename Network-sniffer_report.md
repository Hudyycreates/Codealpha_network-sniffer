# Project Report — Network Sniffer
**Task 1 | CodeAlpha Cybersecurity Internship**

---

## Introduction

This project involved building a network packet sniffer from scratch using Python on a Linux VM. A network sniffer is a tool that captures packets travelling through a network interface and reads their content — including IP addresses, protocols, ports and payload data.

The goal was to understand how data actually moves through a network at a packet level, and to get practical experience with how tools like Wireshark work under the hood.

> 📸 **[ADD SCREENSHOT: VM terminal overview]**

---

## Methodology

The sniffer was built incrementally — one feature at a time — rather than writing everything at once. This made it easier to understand each concept before moving to the next.

**Environment:**
- OS: Ubuntu Linux (VirtualBox VM)
- Language: Python 3.13
- Library: Scapy
- Editor: nano (terminal-based, no GUI)

**Step 1 — Basic packet capture**

Started with the simplest possible version using Scapy's `sniff()` function:

```python
from scapy.all import sniff

def handle_packet(packet):
    print(packet.summary())

sniff(prn=handle_packet, count=10)
```

`sniff()` listens on the network interface and calls `handle_packet()` for every packet that arrives. Even without generating any traffic, the VM was already producing background packets.

> 📸 **[ADD SCREENSHOT: First output showing packet summaries]**

**Step 2 — Extracting IP addresses**

Added the IP layer to read real source and destination addresses:

```python
from scapy.all import sniff, IP

def handle_packet(packet):
    if packet.haslayer(IP):
        src = packet[IP].src
        dst = packet[IP].dst
        print(f"Packet: {src} --> {dst}")
```

`haslayer(IP)` checks if the packet has an IP layer before reading it — not every packet does.

> 📸 **[ADD SCREENSHOT: Output showing real IP addresses]**

**Step 3 — Protocol detection**

Read the protocol number from the IP header and mapped it to a readable name:

```python
proto = packet[IP].proto

if proto == 1:
    print("ICMP")
elif proto == 6:
    print("TCP")
elif proto == 17:
    print("UDP")
```

Protocol numbers are standardised — 1 is always ICMP, 6 is always TCP, 17 is always UDP.

> 📸 **[ADD SCREENSHOT: Output showing protocol names]**

**Step 4 — Port numbers**

Ports live inside TCP and UDP headers, not the IP header. So they are only read inside the correct blocks:

```python
elif proto == 17:
    src_port = packet[UDP].sport
    dst_port = packet[UDP].dport
    print(f"{src} --> {dst} [UDP] {src_port} --> {dst_port}")

elif proto == 6:
    src_port = packet[TCP].sport
    dst_port = packet[TCP].dport
    print(f"{src} --> {dst} [TCP] {src_port} --> {dst_port}")
```

> 📸 **[ADD SCREENSHOT: Output showing port numbers]**

**Step 5 — Payload**

Added the `Raw` layer to read actual data travelling inside packets:

```python
if packet.haslayer(Raw):
    payload = bytes(packet[Raw].load)
    print(f"Payload: {payload}")
```

> 📸 **[ADD SCREENSHOT: Output showing payload data]**

---

## Findings

**Background traffic**
Even with no active browsing, the VM constantly generates traffic:
- UDP port 123 — NTP syncing the system clock
- UDP port 53 — DNS lookups in the background
- ARP broadcasts — checking who else is on the local network

This shows that a device is never truly idle on a network.

**TCP 3-way handshake observed live**
When connecting to a web server, the sniffer captured the full handshake:

```
VM      -->  Server   [TCP]  random port --> 80   (SYN)
Server  -->  VM       [TCP]  80 --> random port   (SYN+ACK)
VM      -->  Server   [TCP]  random port --> 80   (ACK)
```

The VM uses a random ephemeral port as source. The server stays on port 80.

> 📸 **[ADD SCREENSHOT: TCP handshake visible in sniffer output]**

**Payload readable on unencrypted HTTP**
Using `curl http://neverssl.com` in a second terminal, the raw HTML of the webpage was visible in the payload — `<html>`, `<script>` and `<body>` tags all travelling in plain text inside TCP packets.

This demonstrates why HTTP is considered insecure — anyone on the same network can read the data.

> 📸 **[ADD SCREENSHOT: Payload showing HTML content]**

---

## Challenges

**Indentation errors** — Python is strict about indentation. Code placed in the wrong block caused logic errors that were hard to spot visually in nano.

**Variable scope** — defining `src_port` inside a TCP block then referencing it outside caused crashes on ICMP packets where the variable was never defined.

**Timing** — the sniffer and traffic generator need to run simultaneously. Running them one after the other means the packets are already gone by the time the sniffer starts.

**VM environment** — Scapy produces a socket warning in some VM setups. This does not affect functionality but required understanding to not confuse it with a real error.

---

## Security Relevance

- **Unencrypted traffic** — HTTP sends everything in plain text. A sniffer on the same network can read passwords, session tokens and sensitive data with no effort.
- **Port mapping** — port numbers immediately reveal what services are running on a machine. This is the basis of network reconnaissance.
- **Anomaly detection** — unexpected outbound connections, unknown ports or unusual traffic volumes are signs of compromise that a sniffer can help identify.
- **Foundation of Wireshark** — this project replicates the core functionality of professional network analysis tools at a basic level.

---

## What I Would Add Next

- A summary section at the end showing total packets captured, protocol breakdown and most frequent IPs
- Command line filters for protocol or port
- Automatic flagging of suspicious ports or unknown outbound IPs
- Export results to a log file for later analysis

---

## Conclusion

This project gave practical hands-on experience with how network traffic actually works at a packet level. Building the sniffer step by step — rather than using a ready-made tool — made it possible to understand what each layer of a packet contains and why it matters from a security perspective.

Watching a live TCP handshake and reading raw HTML payload from a real website made concepts that are easy to read about suddenly very concrete.
