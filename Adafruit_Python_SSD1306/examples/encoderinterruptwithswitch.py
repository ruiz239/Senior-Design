import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from time import sleep

clk = 17 #Encoder clk pin
dt = 18 #Encoder dt pin
sw=6 #Encoder Switch/Select
DIR = 21   # Direction GPIO Pin
STEP = 20  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 7.5)



paused=False
part="Wrist"

#Initalizing GPIO's of Encoder
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#Initalizing GPIO's of Stepper
GPIO.setwarnings(False)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

#Initializing Microstep Mode pins and Table
MODE = (26, 19, 13)   # Microstep Resolution GPIO Pins
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 1, 1)}
GPIO.output(MODE, RESOLUTION['1/8'])
step_count = SPR*400 #How long loop should last
delay = .0208/2000 #350 is the fastest

#Encoder check states
counter=0
clkLastState = GPIO.input(clk)
dtLastState=GPIO.input(dt)
swLastState=GPIO.input(sw)


#home screen of OLED display
display = Adafruit_SSD1306.SSD1306_128_64(rst=None)
display.begin()
display.clear()
display.display()
displayWidth=display.width
displayHeight=display.height
image=Image.new('1',(displayWidth,displayHeight))
draw=ImageDraw.Draw(image)
font=ImageFont.load_default()
display.clear()
display.display()
converted_count=str(counter)
draw.text((0,0),"Welcome to 5ARA \n Created by: \n Nicholas Ruiz \n Brent Holzhauer \n Mathew Olajide",font=font,fill=255)
display.image(image)
display.display()

def clockwise(stepper,speed,loop):
    for x in range(speed):
        GPIO.output(stepper,GPIO.HIGH)
        sleep(loop)
        GPIO.output(stepper,GPIO.LOW)
        sleep(loop)
    return
#interrupt for + counting 
def clkClicked(channel):
    global counter
    clkState=GPIO.input(clk)
    dtState = GPIO.input(dt)
    
    if clkState ==0 and dtState ==1:
        counter +=1
        print(counter)
        display.begin()
        display.clear()
        display.display()
        displayWidth=display.width
        displayHeight=display.height
        image=Image.new('1',(displayWidth,displayHeight))
        draw=ImageDraw.Draw(image)
        font=ImageFont.load_default()
        converted_count=str(counter)
        draw.text((0,0),"Selected Stepper #" + converted_count,font=font,fill=255)
        draw.text((0,10),"RPM \n" + converted_count,font=font,fill=255)
        display.image(image)
        display.display()
        
#interrupt for -counter         
def dtClicked(channel):
    global counter
    
    clkState =GPIO.input(clk)
    dtState=GPIO.input(dt)
    if clkState ==1 and dtState ==0:
        counter -=1
        print(counter)
        display.begin()
        display.clear()
        display.display()
        displayWidth=display.width
        displayHeight=display.height
        image=Image.new('1',(displayWidth,displayHeight))
        draw=ImageDraw.Draw(image)
        font=ImageFont.load_default()
        converted_count=str(counter)
        draw.text((0,0),"Selected Stepper #" + converted_count,font=font,fill=255)
        draw.text((0,10),"RPM \n" + converted_count,font=font,fill=255)
        display.image(image)
        display.display()

#interrupt for selected button 
def swClicked(channel):
    global paused
    paused = not paused
    convert_paused=str(paused)
    print(paused)
    display.begin()
    display.clear()
    display.display()
    displayWidth=display.width
    displayHeight=display.height
    image=Image.new('1',(displayWidth,displayHeight))
    draw=ImageDraw.Draw(image)
    font=ImageFont.load_default()
    converted_count=str(counter)
    draw.text((0,0),"Selected Stepper #" + converted_count,font=font,fill=255)
    draw.text((0,10),"RPM:" + converted_count,font=font,fill=255)
    draw.text((0,30),"Beginning Arm Movement \n" + part,font=font,fill=255)
    display.image(image)
    display.display()
    if (counter == 3):
        clockwise(20,10000000,.0208/2000)
    if (counter == 6):
        clockwise(20,1000000, .0208/2000)

#call interrupts with certain delay 
GPIO.add_event_detect(clk,GPIO.FALLING,callback=clkClicked,bouncetime=100)
GPIO.add_event_detect(dt,GPIO.FALLING,callback=dtClicked,bouncetime=100)
GPIO.add_event_detect(sw,GPIO.FALLING,callback=swClicked,bouncetime=100)

#send to command line 
raw_input("Welcome to 5ARA \n")

#if statement that intializes movement based on counter
raw_input(counter)



    

