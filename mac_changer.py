import subprocess
import optparse
import re

# optparse terminal icinde kullanicidan input almamiza yarar.
# optparse den parse_object nesnesi olusturduk.
# bu nesne optionslar iceriyor ve bu parse_object = optparse.OptionParser() optionslar *args ve **kwargs alacak

# interface i -i seklinde gostersin diye 2 argument verdik
# kullanicinin girdigi input u da dest=interface e kaydedelim

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i","--interface",dest="interface",help="interface to change !")
    parse_object.add_option("-m","--mac",dest="mac_address",help="new mac address")

    return parse_object.parse_args()

# mac address ve interface i almak istiyoruz, bu yuzden 2 addOptions var
# dest ="interface" --> dedigimiz alinan girdinin nereye kaydedilecegi

# kullanicidan aldigimiz user_interface ve user_mac_address leri asagida kullanacagiz

# terminalden mac adresini degistirmek icin yazdigimiz komutlari burada
# anlamlandirdik bu .py uzantili dosyamizi terminalde calistirmamiz ayni gorevi gorecek.
# subprocess terminalde komut calistirir gibi bilgisayara komut verir.

def change_mac_address(user_interface,user_mac_address):
    subprocess.call(["ifconfig",user_interface,"down"])
    subprocess.call(["ifconfig",user_interface,"hw","ether",user_mac_address])
    subprocess.call(["ifconfig",user_interface,"up"])

# mac adresi degistikten sonra kullaniciya ifconfig calistirip degistigini gosterelim
# herhangi bir metinde filtreleme yapabilmek icin "regex-editor" RegularExpressions kullanacagiz
# mac adresi xx:yy:11:22:zz:aa seklide oldugu icin bir duzen ifade eder, bunu yakalayalim
# import re -->
def control_new_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig",interface])
    new_mac =  re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",str(ifconfig))

    # eger new_mac dogru ise bana bir mac group dondur(string)

    if new_mac:
        return new_mac.group(0)
    else:
        return  None

print("MyMacChanger is started !")

(user_input,arguments) = get_user_input()
change_mac_address(user_input.interface,user_input.mac_address)
control_new_mac(user_input.interface)
finalized_mac = control_new_mac(str(user_input.interface))

if finalized_mac == user_input.mac_address:
    print("Success !")
else:
    print("Error !")

# Kodumuzu terminalde calistirmak icin
# python my_mac_changer.py --interface eth0 --mac 00:aa:22:bb:33:cc
# ornek kod blogunu calistirmaliyiz
