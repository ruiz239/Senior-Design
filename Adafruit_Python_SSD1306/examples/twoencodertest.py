import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from time import sleep

#Encoder 1 
clk = 17 #Encoder clk pin
dt = 18 #Encoder dt pin
sw=6 #Encoder Switch/Select

#Encoder 2
clk2 = 4 #Encoder clk pin
dt2 = 27 #Encoder dt pin

SPR = 200   # Steps per Revolution (360 / 7.5)

paused=False
part="Wrist"
paused2=False
part2="Base"

#Initalizing GPIO's of Encoder
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#Initalizing GPIO's of 2nd Encoder
GPIO.setup(clk2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Initalizing GPIO's of Stepper
GPIO.setwarnings(False)


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
counter2=0
counter=0
clkLastState = GPIO.input(clk)
dtLastState=GPIO.input(dt)
swLastState=GPIO.input(sw)

#2nd encoder check states
clkLastState2 = GPIO.input(clk)
dtLastState2=GPIO.input(dt)
swLastState2=GPIO.input(sw)


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


#Encoder 2 function Add+ 
def clkClicked2(channel):
    global counter2
    clkState2 = GPIO.input(clk2)
    dtState2 = GPIO.input(dt2)
    
    if clkState2 ==0 and dtState2 ==1:
        counter2 +=1
        print(counter2)
        display.begin()
        display.clear()
        display.display()
        displayWidth=display.width
        displayHeight=display.height
        image=Image.new('1',(displayWidth,displayHeight))
        draw=ImageDraw.Draw(image)
        font=ImageFont.load_default()
        converted_count=str(counter)
        converted_count2=str(counter2)
        draw.text((0,0),"Selected Stepper #" + converted_count,font=font,fill=255)
        draw.text((0,10),"RPM \n" + converted_count2,font=font,fill=255)
        display.image(image)
        display.display()

#encoder 2 function subtract -1 
def dtClicked2(channel):
    global counter2
    
    clkState2 =GPIO.input(clk2)
    dtState2=GPIO.input(dt2)
    if clkState2 == 1 and dtState2 == 0:
        counter2 -= 1
        print(counter2)
        display.begin()
        display.clear()
        display.display()
        displayWidth=display.width
        displayHeight=display.height
        image=Image.new('1',(displayWidth,displayHeight))
        draw=ImageDraw.Draw(image)
        font=ImageFont.load_default()
        converted_count=str(counter)
        converted_count2=str(counter2)
        draw.text((0,0),"Selected Stepper #" + converted_count,font=font,fill=255)
        draw.text((0,10),"RPM \n" + converted_count2,font=font,fill=255)
        display.image(image)
        display.display()
        
#stepper function for clockwise rotation #add enable
def clockwise(stepper,speed,loop,direction,clockwise):
    GPIO.setup(direction, GPIO.OUT)
    GPIO.setup(stepper, GPIO.OUT)
    for x in range(speed):
        GPIO.output(direction,clockwise)
        GPIO.output(stepper,GPIO.HIGH)
        sleep(loop)
        GPIO.output(stepper,GPIO.LOW)
        sleep(loop)
    return

#interrupt for + counting 
def clkClicked(channel):
    global counter
    global counter2
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
        converted_count2=str(counter2)
        draw.text((0,0),"Selected Stepper #" + converted_count,font=font,fill=255)
        draw.text((0,10),"RPM \n" + converted_count2,font=font,fill=255)
        display.image(image)
        display.display()
        
#interrupt for -counter         
def dtClicked(channel):
    global counter
    global counter2
    
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
        converted_count2=str(counter2)
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
    converted_count2=str(counter2)
    draw.text((0,0),"Selected Stepper #" + converted_count,font=font,fill=255)
    draw.text((0,10),"RPM:" + converted_count2,font=font,fill=255)
    draw.text((0,30),"Beginning Arm Movement \n" + part,font=font,fill=255)
    display.image(image)
    display.display()
    if (counter == 3 and paused == True):
        clockwise(20,1000,.0208/(50*counter2),16,1)
        sleep(.5)
    elif (counter ==3 and paused == False):
        clockwise(20,1000,.0208/(50*counter2),16,0)
        sleep(.5)
    if (counter == 6 and paused == True):
        clockwise(20,50000, .0208/(50*counter2),21,CCW)
        
        
#call interrupts with certain delay 
GPIO.add_event_detect(clk,GPIO.FALLING,callback=clkClicked,bouncetime=100)
GPIO.add_event_detect(dt,GPIO.FALLING,callback=dtClicked,bouncetime=100)
GPIO.add_event_detect(sw,GPIO.FALLING,callback=swClicked,bouncetime=100)
GPIO.add_event_detect(clk2,GPIO.FALLING,callback=clkClicked2,bouncetime=100)
GPIO.add_event_detect(dt2,GPIO.FALLING,callback=dtClicked2,bouncetime=100)

#send to command line 
raw_input("Welcome to 5ARA \n")

#if statement that intializes movement based on counter
raw_input(counter)



    


