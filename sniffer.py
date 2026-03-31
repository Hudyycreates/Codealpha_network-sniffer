from scapy.all import sniff, IP, UDP, TCP, Raw

def handle_packet(packet):
	if packet.haslayer(IP):

		src = packet[IP].src
		dst = packet[IP].dst
		proto = packet[IP].proto
		

		if proto == 1:
			print (f" packet {src} --> {dst} [ICMP]")

		elif proto == 17:
			print("UDP")
			src_port = packet[UDP].sport
			dst_port = packet[UDP].dport
			print (f" packet: {src} --> {dst} [UDP]: {src_port} --> {dst_port}")

			if packet.haslayer[Raw]:
				payload = bytes(packet[Raw].load)
				print (f" payload {payload}")

		elif proto == 6:
			print("TCP")
			src_port = packet[TCP].sport
			dst_port = packet[TCP].dport
			print (f" packet: {src} --> {dst} [TCP]: {src_port} --> {dst_port}")

			if packet.haslayer[Raw]:
				payload = bytes(packet[Raw].load)
				print (f" payload: {payload}" )

		else:
			print (f" packet {srs} --> {dst} [OTHER]")

sniff (prn=handle_packet, count=50)


