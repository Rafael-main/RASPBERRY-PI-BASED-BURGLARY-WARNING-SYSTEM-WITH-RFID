# Include the library files
import I2C_LCD_driver # WALAON RANI PUHON
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from time import sleep
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import requests
import json
from datetime import datetime


#Include the buzzer pin
buzzer = 19

#Include the relay pin
relay = 26

#Enter your tag ID
Tag_ID = "1044051400610"

door = True

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)

# Create a object for the LCD
lcd = I2C_LCD_driver.lcd() # WALAON RANI PUHON

# Create a object for the RFID module
read = SimpleMFRC522()

#Starting text WALAON RANI PUHON
lcd.lcd_display_string("Door lock system",1,0)
for a in range (0,15):
    lcd.lcd_display_string(".",2,a)
    sleep(0.1)


# for email
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()

valid_entries = ["Cody"]

id = 0
text = ""
server_address = 'http://192.168.0.108:5000'
headers = {'Content-type': 'application/json', 'Accept':'text/plain'}

def send_email(content):

    server.login('lockdoor.monitoring@gmail.com','Aiwprton.1')
    server.sendmail('lockdoor.monitoring@gmail.com','eduard-alexandru.codau@student.tuiasi.ro',content.as_string())

def send_post_to_server(json_text):
    requests.post(server_address,data=json_text, headers=headers)

def read():
    global id
    global text

    t = threading.Thread(target=display_waiting_text)
    t.start()
  
    id, text = reader.read()
    t.join()
    
    print(id)
    print(text)
    
    if str(text.split(" ")[0]) in valid_entries:
        GPIO.output(13, GPIO.HIGH)
        
        lcd.lcd_display_string("Acces granted: " + text,1)
        json_text = json.dumps({"name": str(text.split(" ")[0]), "time": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")), "status":"granted"})
        t1 = threading.Thread(target=send_post_to_server,args=(json_text,))
        t1.start()
        
        message = MIMEMultipart()
        message['From'] = 'lockdoor.monitoring@gmail.com'
        message['To'] = 'eduard-alexandru.codau@student.tuiasi.ro'
        message['Subject'] = 'Monitoring notification'
        email = "La data de " + str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")) + " utilizatorul " + str(text.split(" ")[0]) + " a incercat sa acceseze sistemul. Rezultat: granted"
        message.attach(MIMEText(email,'plain'))
        
        t2 = threading.Thread(target=send_email,args=(message,))
        t2.start()
        
        servo.unlock()
        sleep(5)
        GPIO.output(13, GPIO.LOW)
        servo.lock()
    else:
        print(text)
        GPIO.output(11, GPIO.HIGH)
        lcd.lcd_display_string("Acces denied: " + text,1)
        json_text = json.dumps({"name": str(text.split(" ")[0]), "time": str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")), "status":"denied"})
        t1 = threading.Thread(target=send_post_to_server, args=(json_text,))
        t1.start();
        
        message = MIMEMultipart()
        message['From'] = 'lockdoor.monitoring@gmail.com'
        message['To'] = 'eduard-alexandru.codau@student.tuiasi.ro'
        message['Subject'] = 'Monitoring notification'
        email = "La data de " + str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")) + " utilizatorul " + str(text.split(" ")[0]) + " a incercat sa acceseze sistemul. Rezultat: denied"
        message.attach(MIMEText(email,'plain'))
        
        t2 = threading.Thread(target=send_email,args=(message,))
        t2.start()
        sleep(3)
        GPIO.output(11, GPIO.LOW)

    id = 0
    text = ""

while True:
    lcd.lcd_clear()
    lcd.lcd_display_string("Place your Tag",1,1)
    id,Tag = read.read()
    
    id = str(id)
               
    if id == Tag_ID:
        lcd.lcd_clear()
        lcd.lcd_display_string("Successful",1,3)
        
        if door == True:
            lcd.lcd_display_string("Door is locked",2,1)
            GPIO.output(relay,GPIO.HIGH)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.5)
            GPIO.output(buzzer,GPIO.LOW)
            door = False
            sleep(3)
            
            
        elif door == False:
            lcd.lcd_display_string("Door is open",2,2)
            GPIO.output(relay,GPIO.LOW)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.5)
            GPIO.output(buzzer,GPIO.LOW)
            door = True
            sleep(3)
                        
        
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string("Wrong Tag!",1,3)
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.3)
        GPIO.output(buzzer,GPIO.LOW)
        sleep(0.3)
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.3)
        GPIO.output(buzzer,GPIO.LOW)
        sleep(0.3)
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.3)
        GPIO.output(buzzer,GPIO.LOW)            

GPIO.cleanup()     
        
