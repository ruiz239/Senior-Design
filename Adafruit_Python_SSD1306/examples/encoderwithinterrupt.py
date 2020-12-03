import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from time import sleep

clk = 17
dt = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

clkLastState = GPIO.input(clk)

def my_callback(channel):
    global clkLastState
    global counter
    try:
        clkState = GPIO.input(clk)
        if clkState != clkLastState:
            dtState=GPIO.input(dt)
            if dtState != clkState:
                counter += 1
            else:
                counter -= 1
            print (counter)
            clkLastState = clkState
    finally:
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
        draw.text((0,0),"Current Motor Selected\n" + converted_count,font=font,fill=255)
        display.image(image)
        display.display()

counter =0
clkLastState = GPIO.input(clk)
GPIO.add_event_detect(17,GPIO.FALLING,callback=my_callback,bouncetime=300)


