import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from time import sleep

display = Adafruit_SSD1306.SSD1306_128_64(rst=None)
display.begin()
display.clear()
display.display()
displayWidth=display.width
displayHeight=display.height
image=Image.new('1',(displayWidth,displayHeight))
draw=ImageDraw.Draw(image)
font=ImageFont.load_default()
draw.text((0,0),"Welcome to 5ARA",font=font,fill=255)
display.image(image)
display.display()

clk = 17
dt = 18

counter=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


clkLastState = GPIO.input(clk)

try:

        while True:
            display.clear()
            display.display()
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                if dtState != clkState:
                    counter += 1
                else:
                    counter -= 1
                    
                print (counter)
                clkLastState = clkState
                sleep(0.01)
                display.clear()
                display.display()
                converted_count=str(counter)
                draw.text((0,0),"Current Motor Selected\n" + converted_count,font=font,fill=255)
                display.image(image)
                display.display()


finally:
        GPIO.cleanup()


