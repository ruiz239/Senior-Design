import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

step = 16
direction = 7

paused = False
cworccw = ''
#Function for setting all drivers to SLEEP
def Setup(Enable):
    GPIO.setup(Enable,GPIO.OUT)
    GPIO.output(Enable,GPIO.HIGH) #Sleeping Driver
    return
#Call function to setup driver state enable
Setup(10)
Setup(9)
Setup(11)
Setup(5)
Setup(12)

#Encoder 1 
clk = 17 #Encoder clk pin
dt = 18 #Encoder dt pin
sw=6 #Encoder Switch/Select

#Encoder 2
clk2 = 21 #Encoder clk pin
dt2 = 20 #Encoder dt pin

#Encoder 3
clk3=14
dt3=15

SPR = 200   # Steps per Revolution (360 / 1.8) given by datasheet

#Initalizing GPIO's of Encoder
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sw,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#Initalizing GPIO's of 2nd Encoder
GPIO.setup(clk2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Initalizing GPIO's of 3rd Encoder
GPIO.setup(clk3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

#Encoder Values
counter3=0
counter2=0 #is incremented based on encoder 2 + or - 
counter=0 # is incremented based on encoder 1 + or -

#1st encder check states
clkLastState = GPIO.input(clk)
dtLastState=GPIO.input(dt)
swLastState=GPIO.input(sw)

#2nd encoder check states
clkLastState2 = GPIO.input(clk)
dtLastState2=GPIO.input(dt2)


#3rd Encoder check states
clkLastState3 = GPIO.input(clk)
dtLastState3=GPIO.input(dt3)

#home screen of OLED display
#Initalize display with Title Screen
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

def LCD():
    if paused == True:
        cworccw = 'CW'
    elif paused == False:
        cworccw = 'CCW'
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
    converted_count3=str(counter3)
    draw.text((0,0),"Selected Stepper #" + converted_count,font=font,fill=255)
    draw.text((0,10),"RPM =" + converted_count2,font=font,fill=255)
    draw.text((0,30),"# of Steps  = " + converted_count3,font=font,fill=255)
    draw.text((0,50),"Direction = " + cworccw,font=font,fill=255)
    display.image(image)
    display.display()

#Encoder 2 function Add+ 
def clkClicked2(channel):
    global counter2
    clkState2 = GPIO.input(clk2)
    dtState2 = GPIO.input(dt2)
    
    #if Encoder is counting up count +1 and refresh OLED screen 
    if clkState2 ==0 and dtState2 ==1:
        counter2 +=1
        print(counter2)
        LCD()
    
        

#Encoder 3 
def clkClicked3(channel):
    global counter3
    clkState3 = GPIO.input(clk3)
    dtState3 = GPIO.input(dt3)
    
    #if Encoder is counting up count +1 and refresh OLED screen 
    if clkState3 ==0 and dtState3 ==1:
        counter3 +=1
        print(counter3)
        LCD()
        
        #Stepper one clockwise loop ##### Figure out each stepper enable pin 
        if (counter == 3 and paused == True):
            Setup(9)
            Setup(11)
            Setup(5)
            Setup(12)
            clockwise(10,step,counter3*10,.0208/50*abs(counter2),direction,1)
            sleep(.5)
        
        #Stepper two Clockwise Loop 
        elif (counter == 6 and paused == True):
            Setup(10)
            Setup(12)
            Setup(11)
            Setup(5)
            clockwise(9,step,counter3*10,.0208/(50*abs(counter2)),direction,1)
            sleep(.5)
        
        #Stepper three clockwise loop
        elif (counter == 9 and paused == True):
            Setup(10)
            Setup(12)
            Setup(9)
            Setup(5)
            clockwise(11,step,counter3*10,.0208/(50*abs(counter2)),direction,1)
            sleep(.5)
        
        #Stepper four clockwise loop
        elif (counter == 12 and paused == True):
            Setup(10)
            Setup(9)
            Setup(11)
            Setup(12)
            clockwise(5,step,counter3*10,.0208/(50*abs(counter2)),direction,1)
            sleep(.5)
        
        #Stepper five clockwise loop 
        elif (counter == 15 and paused == True):
            Setup(10)
            Setup(9)
            Setup(11)
            Setup(5)
            clockwise(12,step,counter3*10,.0208/(50*abs(counter2)),direction,1)
            sleep(.5)
        
#encoder 2 function subtract -1 
def dtClicked2(channel):
    global counter2
    
    clkState2 =GPIO.input(clk2)
    dtState2=GPIO.input(dt2)
    #if second encoder is being subtracted count down and refresh OLED
    if clkState2 == 1 and dtState2 == 0:
        counter2 -= 1
        print(counter2)
        LCD()
        
def dtClicked3(channel):
    global counter3
    
    clkState3 =GPIO.input(clk3)
    dtState3=GPIO.input(dt3)
    #if second encoder is being subtracted count down and refresh OLED
    if clkState3 == 1 and dtState3 == 0:
        counter3 -= 1
        print(counter3)
        LCD()
        
        #Stepper one CCW Loop 
         #Stepper one clockwise loop ##### Figure out each stepper enable pin 
        if (counter == 3 and paused == True):
            Setup(9)
            Setup(11)
            Setup(5)
            Setup(12)
            clockwise(10,step,counter3*10,.0208/50*abs(counter2),direction,0)
            sleep(.5)
        
        #Stepper two Clockwise Loop 
        elif (counter == 6 and paused == True):
            Setup(10)
            Setup(12)
            Setup(11)
            Setup(5)
            clockwise(9,step,counter3*10,.0208/(50*abs(counter2)),direction,0)
            sleep(.5)
        
        #Stepper three clockwise loop
        elif (counter == 9 and paused == True):
            Setup(10)
            Setup(12)
            Setup(9)
            Setup(5)
            clockwise(11,step,counter3*10,.0208/(50*abs(counter2)),direction,0)
            sleep(.5)
        
        #Stepper four clockwise loop
        elif (counter == 12 and paused == True):
            Setup(10)
            Setup(9)
            Setup(11)
            Setup(12)
            clockwise(5,step,counter3*10,.0208/(50*abs(counter2)),direction,0)
            sleep(.5)
        
        #Stepper five clockwise loop 
        elif (counter == 15 and paused == True):
            Setup(10)
            Setup(9)
            Setup(11)
            Setup(5)
            clockwise(12,step,counter3*10,.0208/(50*abs(counter2)),direction,1)
            sleep(.5)
        
#stepper function for clockwise rotation #setup enable
def clockwise(Enable,stepper,speed,loop,direction,clockwise):
    GPIO.setup(Enable,GPIO.OUT) #Setting up enable pin
    GPIO.setup(direction, GPIO.OUT) #declare direction pin
    GPIO.setup(stepper, GPIO.OUT) #declare stepper pin 
    GPIO.output(direction,clockwise) #clockwise = 0 and ccw=1
    GPIO.output(Enable,GPIO.LOW) #Enabling Driver
    for x in range(speed):
        GPIO.output(stepper,GPIO.HIGH) #pulse sent high 
        sleep(loop) #pulse length
        GPIO.output(stepper,GPIO.LOW) #pulse sent low
        sleep(loop) #delay until next pulse
    return

#interrupt for Encoder 1 + counting 
def clkClicked(channel):
    global counter
    global counter2
    clkState=GPIO.input(clk)
    dtState = GPIO.input(dt)
    
    #if encoder 1 is adding + then refresh OLED 
    if clkState ==0 and dtState ==1:
        counter +=1
        print(counter)
        LCD()
        
#interrupt for Encoder 1 subtractg          
def dtClicked(channel):
    global counter
    global counter2
    
    clkState =GPIO.input(clk)
    dtState=GPIO.input(dt)
    #if encoder is subtracting then refresh oled with updates 
    if clkState ==1 and dtState ==0:
        counter -=1
        print(counter)
        LCD()

#interrupt for button on encoder 1 pressed...
def swClicked(channel):
    global paused
    paused = not paused
    #renew display with updated content
    LCD()

#call interrupts with certain delay 
#Encoder 1 
GPIO.add_event_detect(clk,GPIO.FALLING,callback=clkClicked,bouncetime=100)
GPIO.add_event_detect(dt,GPIO.FALLING,callback=dtClicked,bouncetime=100)
GPIO.add_event_detect(sw,GPIO.FALLING,callback=swClicked,bouncetime=100)

#Encoder 2 
GPIO.add_event_detect(clk2,GPIO.FALLING,callback=clkClicked2,bouncetime=100)
GPIO.add_event_detect(dt2,GPIO.FALLING,callback=dtClicked2,bouncetime=100)

#Encoder 3 
GPIO.add_event_detect(clk3,GPIO.FALLING,callback=clkClicked3,bouncetime=100)
GPIO.add_event_detect(dt3,GPIO.FALLING,callback=dtClicked3,bouncetime=100)



#send to Terminal command line 
raw_input("Welcome to 5ARA \n")
raw_input("Counter 1 value" + counter)
raw_input("Counter 2 value" + counter2)



    







