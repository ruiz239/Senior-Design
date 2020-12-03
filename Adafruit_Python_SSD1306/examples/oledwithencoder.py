from time import sleep
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

count=13
speed=55 
converted_count=str(count)
converted_speed=str(speed)

display = Adafruit_SSD1306.SSD1306_128_64(rst=None)

display.begin()
display.clear()
display.display()
displayWidth=display.width
displayHeight=display.height
image=Image.new('1',(displayWidth,displayHeight))
draw=ImageDraw.Draw(image)
font=ImageFont.load_default()

draw.text((0,0),"Current Motor Selected\n" + converted_count,font=font,fill=255)
draw.text((0,30),"Current Speed\n" + converted_speed,font=font,fill=255)

display.image(image)
display.display()

