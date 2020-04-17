import scapy.all as scapy
import optparse

# mac ve ip adrelerini eslestirebilmek icin ARP request kullanacagiz
# broadcast yapip gelen cevabi alacagiz(arp response) ve yazdiracagiz

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i","--ipaddress",dest="ip_address",help="Enter Ip Address")

    (user_input,arguments) = parse_object.parse_args()
    # user_input ta ip_address bilgisi girilmediyse
    if not user_input.ip_address:
        print("Enter Ip Address")
    return user_input

def scan_my_network(ip):
    # scapy.ls () verilen parametredeki fonksiyonun nasil kullanilacagini gosterir
    # scapy.ls(scapy.ARP())
    # bunun icin terminalde my_net_scanner calistiralim

    arp_request_packet = scapy.ARP(pdst=ip)

    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # broadcast destinationumuz ff herkese gidecek
    # 2 paketi tek paket haline getirdik asagida

    combined_packet = broadcast_packet/arp_request_packet

    (answered_list,unanswered_list) = scapy.srp(combined_packet,timeout=1)
    answered_list.summary()
    # paketleri gonderip cevaplari alalim

user_ip_address = get_user_input()
scan_my_network(user_ip_address.ip_address)