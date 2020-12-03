import RPi.GPIO as GPIO
from time import sleep

clk = 17
dt = 18
sw=6

counter=0

def button_callback(channel):
    print("button was pushed!")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(sw,GPIO.RISING,callback=button_callback)
    message = input("Press enter to quit \n\n")
    GPIO.cleanup()



