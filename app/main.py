from flask import Blueprint, redirect, render_template, url_for, session
from . import db
from app import app

#import time
#import RPi.GPIO as GPIO
#import I2C_LCD_driver
#from mfrc522 import SimpleMFRC522
#from time import sleep
# from gpiozero import MotionSensor

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('welcome'))

@main.route('/home')
def home():
    if 'user' in session:

        # pir = MotionSensor(4)

        # while True:
## 	pir.wait_for_motion()
## 	print("You moved")
## 	pir.wait_for_no_motion()


#relay = 18;
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setuprelay(GPIO.OUT)
#GPIO.output(relay , 0)


##Include the buzzer pin
#buzzer = 19

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(buzzer,GPIO.OUT)

## Create a object for the LCD
#lcd = I2C_LCD_driver.lcd()

## Create a object for the RFID module
#scan = SimpleMFRC522()


#try:
#        print("Now place your Tag to scan")      
#        lcd.lcd_display_string("Place your Tag",1,1)                                               
#        scan.write("Tag ID")
#        id,Tag = scan.read()                    
#        print("Your Tag ID is : " + str(id))
#        lcd.lcd_clear()
#        lcd.lcd_display_string("Tag ID",1,5)
#        lcd.lcd_display_string(str(id),2,1)
    
#        GPIO.output(buzzer,GPIO.HIGH)
#        sleep(0.5)
#        GPIO.output(buzzer,GPIO.LOW)

#finally:
#        GPIO.cleanup()
        

##Uses methods from motors.py to send commands to the GPIO to operate the motors
#@app.route('/<changepin>', methods=['POST'])
#def reroute(changepin):
#    changePin = int(changepin) #cast changepin to an int
#    if changePin == 1:
#        print "ON"
#                GPIO.output( relay , 1)                
#    elif changePin == 2:
#        print "OFF"
#                GPIO.output(relay, 0)
#    response = make_response(redirect(url_for('index')))
#    return(response)


        return render_template('home.html')
    return redirect(url_for('welcome'))


@main.route('/table')
def table():
    return render_template('table.html')


