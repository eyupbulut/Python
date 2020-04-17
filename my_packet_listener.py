import scapy.all as scapy
from scapy_http import http

# arp saldirisinde gonderilen paketleri wireshark ile de dinleyebiliriz.
# eth0 a tiklayarak data akisini izleyebiliriz. "pip install scapy_http kur.
# gelen paketleri dinleyip kendimize cekecegiz-sniffing

def listen_packets(interface):
    scapy.sniff(iface=interface,store=False,prn=analyze_packets)
    # prn=callback function - herhangi bir durum oldugunda nasil devam edecegimizi soyler

# layerleri inceleyerek aradigimiz bilgilerin bulundugu katmanlara ulasmaliyiz
def analyze_packets(packet):
    #packet.show()
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)
listen_packets("eth0")