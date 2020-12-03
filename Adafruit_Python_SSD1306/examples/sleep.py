import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

x=3 
def Setup(Enable):
    GPIO.setup(Enable,GPIO.OUT)
    GPIO.output(Enable,GPIO.HIGH) #Sleeping Driver
    return
    

def clockwise(Enable,stepper,speed,loop,direction,clockwise):
    GPIO.output(Enable,GPIO.LOW) #Enabling Driver
    for x in range(speed):
        GPIO.output(stepper,GPIO.HIGH) #pulse sent high 
        sleep(loop) #pulse length
        GPIO.output(stepper,GPIO.LOW) #pulse sent low
        sleep(loop) #delay until next pulse
    return

Setup(14)
while True:
    clockwise(14,20,1000,16,0)
