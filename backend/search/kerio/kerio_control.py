import os
from flask import Flask, request, render_template, redirect, url_for
from scapy.all import sniff, IP
import threading

# Fayl nomlari
TERMS_FILE = "terms.txt"
LOG_FILE = "traffic.log"
BLOCKED_IPS_FILE = "blocked_ips.txt"
PORT_RULES_FILE = "port_rules.txt"
DISABLED_TERMS_FILE = "disabled_terms.txt"

# Flask ilovasi
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Terminlarni yuklash
def load_terms():
    with open(TERMS_FILE, "r") as file:
        return [line.strip() for line in file.readlines()]

# Bloklangan IPlarni yuklash
def load_blocked_ips():
    with open(BLOCKED_IPS_FILE, "r") as file:
        return [line.strip() for line in file.readlines()]

# Port qoidalarini yuklash
def load_port_rules():
    rules = {}
    with open(PORT_RULES_FILE, "r") as file:
        for line in file:
            if ":" in line:
                port, action = line.strip().split(":")
                rules[int(port)] = action
    return rules

# To'xtatilgan qoidalarni yuklash
def load_disabled_terms():
    if not os.path.exists(DISABLED_TERMS_FILE):
        with open(DISABLED_TERMS_FILE, "w") as file:
            pass
    with open(DISABLED_TERMS_FILE, "r") as file:
        return [line.strip() for line in file.readlines()]

# Paketlarni tekshirish
def check_packet(packet):
    # IP va port qoidalari
    if packet.haslayer(IP):
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        blocked_ips = load_blocked_ips()

        if ip_src in blocked_ips or ip_dst in blocked_ips:
            with open(LOG_FILE, "a") as log_file:
                log_file.write(f"Blocked IP: {ip_src if ip_src in blocked_ips else ip_dst}\n")
            print(f"Blocked IP detected: {ip_src if ip_src in blocked_ips else ip_dst}")
            return

    # Terminlarni tekshirish
    if packet.haslayer("Raw"):
        raw_data = packet["Raw"].load.decode(errors="ignore")
        terms = load_terms()
        disabled_terms = load_disabled_terms()
        active_terms = [term for term in terms if term not in disabled_terms]
        for term in active_terms:
            if term in raw_data:
                with open(LOG_FILE, "a") as log_file:
                    log_file.write(f"Blocked term: {term} in packet: {packet.summary()}\n")
                print(f"Blocked term found: {term}")
                return

# Tarmoq trafikini kuzatish
def start_sniffing():
    print("Sniffing started...")
    sniff(filter="tcp", prn=check_packet, store=False)

# Windowsda IP manzilini bloklash (netsh)
def block_ip_windows(ip):
    command = f"netsh advfirewall firewall add rule name=\"Block {ip}\" dir=in action=block remoteip={ip}"
    os.system(command)
    print(f"IP {ip} is blocked.")

# Windowsda IP manzilini bloklashni olib tashlash (netsh)
def unblock_ip_windows(ip):
    command = f"netsh advfirewall firewall delete rule name=\"Block {ip}\""
    os.system(command)
    print(f"IP {ip} is unblocked.")

# Flask yo‘llari
@app.route('/')
def home():
    terms = load_terms()
    disabled_terms = load_disabled_terms()
    blocked_ips = load_blocked_ips()
    port_rules = load_port_rules()
    return render_template("index.html", terms=terms, disabled_terms=disabled_terms, blocked_ips=blocked_ips, port_rules=port_rules)

@app.route('/add_term', methods=['POST'])
def add_term():
    term = request.form.get('term')
    if term:
        with open(TERMS_FILE, "a") as file:
            file.write(term + "\n")
    return redirect(url_for('home'))

@app.route('/remove_term', methods=['POST'])
def remove_term():
    term = request.form.get('term')
    terms = load_terms()
    if term in terms:
        terms.remove(term)
        with open(TERMS_FILE, "w") as file:
            file.write("\n".join(terms))
    return redirect(url_for('home'))

@app.route('/disable_term', methods=['POST'])
def disable_term():
    term = request.form.get('term')
    terms = load_terms()
    disabled_terms = load_disabled_terms()
    if term in terms and term not in disabled_terms:
        with open(DISABLED_TERMS_FILE, "a") as file:
            file.write(term + "\n")
    return redirect(url_for('home'))

@app.route('/enable_term', methods=['POST'])
def enable_term():
    term = request.form.get('term')
    disabled_terms = load_disabled_terms()
    if term in disabled_terms:
        disabled_terms.remove(term)
        with open(DISABLED_TERMS_FILE, "w") as file:
            file.write("\n".join(disabled_terms))
    return redirect(url_for('home'))

@app.route('/add_ip', methods=['POST'])
def add_ip():
    ip = request.form.get('ip')
    if ip:
        with open(BLOCKED_IPS_FILE, "a") as file:
            file.write(ip + "\n")
        
        # Windowsda IPni bloklash
        block_ip_windows(ip)
    return redirect(url_for('home'))

@app.route('/remove_ip', methods=['POST'])
def remove_ip():
    ip = request.form.get('ip')
    blocked_ips = load_blocked_ips()
    if ip in blocked_ips:
        blocked_ips.remove(ip)
        with open(BLOCKED_IPS_FILE, "w") as file:
            file.write("\n".join(blocked_ips))
        
        # Windowsda IPni bloklashni olib tashlash
        unblock_ip_windows(ip)
    return redirect(url_for('home'))

@app.route('/add_port_rule', methods=['POST'])
def add_port_rule():
    port = request.form.get('port')
    action = request.form.get('action')
    if port and action:
        with open(PORT_RULES_FILE, "a") as file:
            file.write(f"{port}:{action}\n")
    return redirect(url_for('home'))

@app.route('/remove_port_rule', methods=['POST'])
def remove_port_rule():
    port = request.form.get('port')
    port_rules = load_port_rules()
    port = int(port)
    if port in port_rules:
        del port_rules[port]
        with open(PORT_RULES_FILE, "w") as file:
            for p, a in port_rules.items():
                file.write(f"{p}:{a}\n")
    return redirect(url_for('home'))

if __name__ == "__main__":
    sniffing_thread = threading.Thread(target=start_sniffing, daemon=True)
    sniffing_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)
