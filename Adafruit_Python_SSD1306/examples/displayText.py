import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from time import sleep

DIR = 21   # Direction GPIO Pin
STEP = 20  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 200   # Steps per Revolution (360 / 7.5)

clk = 17
dt = 18

counter=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)
MODE = (26, 19, 13)   # Microstep Resolution GPIO Pins
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 1, 1)}
GPIO.output(MODE, RESOLUTION['1/8'])
step_count = SPR*400
delay = .0208/2000 #350 is the fastest



clkLastState = GPIO.input(clk)

try:

        while True:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                if dtState != clkState:
                    counter += 1
                    if (counter == 3):
                        for x in range(step_count):
                            GPIO.output(DIR,CCW)
                            GPIO.output(STEP, GPIO.HIGH)
                            sleep(delay)
                            GPIO.output(STEP, GPIO.LOW)
                            sleep(delay)
                            if (counter > 4):
                                break
                else:
                    counter -= 1
                    if (counter ==6):
                        for x in range(step_count):
                            GPIO.output(DIR,CW)
                            GPIO.output(STEP, GPIO.HIGH)
                            sleep(delay)
                            GPIO.output(STEP, GPIO.LOW)
                            sleep(delay)
                            if (counter > 4):
                                break
                print (counter)
                clkLastState = clkState
                sleep(0.01)
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





finally:
        GPIO.cleanup()

