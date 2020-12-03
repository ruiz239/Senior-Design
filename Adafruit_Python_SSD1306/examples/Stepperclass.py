import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self,Ena,Step,Direction,Mode0,RESOLUTION):
        GPIO.setmode(GPIO.BCM)
        self.Ena=Ena
        self.Step=Step
        self.Direction=Direction
        self.Mode0=Mode0
        self.RESOLUTION=RESOLUTION
        GPI0.setup(self.Ena, GPIO.OUT)
        GPIO.setup(self.Direction, GPIO.OUT)
        GPIO.setup(self.Step, GPIO.OUT)
        GPIO.setup(self.Mode0,GPIO.OUT)
        
    def Stepper(self,step_count=1000,delay=.0208/32):
        self.RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 1, 1)}
        GPIO.output(self.Mode0, self.RESOLUTION)
        for x in range(step_count):
            GPIO.output(self.Direction,1)
            GPIO.output(self.Step,GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.Step,GPIO.LOW)
            sleep(delay)
            
while True:
    m1=Motor(12,16,20,(26,19,13),('1/8'))
    m1.Stepper()
            
        
    
        