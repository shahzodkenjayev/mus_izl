from scapy.all import sniff
import re

TERMS_FILE = "terms.txt"

# Terminlarni yuklash
def load_terms():
    with open(TERMS_FILE, "r") as file:
        return [line.strip() for line in file.readlines()]

# Paketlarni qayta ishlash
def process_packet(packet):
    if packet.haslayer("Raw"):
        raw_data = packet["Raw"].load.decode(errors="ignore")
        terms = load_terms()
        for term in terms:
            if term in raw_data:
                print(f"[Filtrlashga mos] Topildi: {term}")
                with open("filtered_packets.log", "a") as log_file:
                    log_file.write(f"{packet.summary()}\n")

# Tarmoq paketlarini kuzatish
def start_sniffing():
    print("Tarmoqni kuzatish boshlandi...")
    sniff(filter="tcp", prn=process_packet, store=False)
