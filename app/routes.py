## First import the Flask, render_template, request, redirect, url_for, make_response classes from flask library.
import simplejson as json
from datetime import datetime
import base64
from app import app


from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session
import time
import RPi.GPIO as GPIO
import I2C_LCD_driver
from mfrc522 import SimpleMFRC522
from time import sleep

# from gpiozero import MotionSensor

# pir = MotionSensor(4)

# while True:
# 	pir.wait_for_motion()
# 	print("You moved")
# 	pir.wait_for_no_motion()


relay = 18;
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setuprelay(GPIO.OUT)
GPIO.output(relay , 0)


#Include the buzzer pin
buzzer = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzzer,GPIO.OUT)

# Create a object for the LCD
lcd = I2C_LCD_driver.lcd()

# Create a object for the RFID module
scan = SimpleMFRC522()


try:
        print("Now place your Tag to scan")      
        lcd.lcd_display_string("Place your Tag",1,1)                                               
        scan.write("Tag ID")
        id,Tag = scan.read()                    
        print("Your Tag ID is : " + str(id))
        lcd.lcd_clear()
        lcd.lcd_display_string("Tag ID",1,5)
        lcd.lcd_display_string(str(id),2,1)
    
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)

finally:
        GPIO.cleanup()
        


@app.route('/')
def index():
    return render_template('index.html')

#Uses methods from motors.py to send commands to the GPIO to operate the motors
@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):
    changePin = int(changepin) #cast changepin to an int
    if changePin == 1:
        print "ON"
                GPIO.output( relay , 1)                
    elif changePin == 2:
        print "OFF"
                GPIO.output(relay, 0)
    response = make_response(redirect(url_for('index')))
    return(response)



@app.route("/signup")
def signup():
	if "username" in session and "accountType" in session:
		return redirect(url_for("profile"))
	else:
		return render_template("signup.html",title="Signup to Panimalay")

@app.route("/signin")
def signin():
	if "username" in session and "accountType" in session:
		return redirect(url_for("profile"))
	else:
		return render_template("signin.html",title="Signin to Panimalay")

