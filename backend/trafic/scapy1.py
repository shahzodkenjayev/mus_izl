from scapy.all import sniff, IP, TCP

def packet_callback(packet):
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            print(f"[+] TCP Packet: {src_ip}:{tcp_layer.sport} -> {dst_ip}:{tcp_layer.dport}")
        else:
            print(f"[+] IP Packet: {src_ip} -> {dst_ip}")

# Paketlarni kuzatish (root huquqlari talab etiladi)
sniff(filter="ip", prn=packet_callback, store=0)
