import board
import touchio
import neopixel
import time
import digitalio
from rainbowio import colorwheel
import random

# LED Colors
YELLOW = (221, 240, 12)
PURPLE = (213, 12, 240)
RED = (255, 0, 0)
BLUE = (12, 39, 240)
GREEN = (0,255,0)
ORANGE = (255,165,0)
TEAL = (0,128,128)
CYAN = (0,255,255)
LIGHTBLUE = (30,144,255)
PINK = (255,105,180)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

colorList = [
    YELLOW, 
    PURPLE,
    RED,
    BLUE,
    GREEN,
    ORANGE,
    TEAL,
    CYAN,
    LIGHTBLUE,
    PINK,
    WHITE
]
colorIndex = 0
colorListMax = len(colorList) 

# random colors
r = random.randrange(10, 255)
g = random.randrange(10, 255)
b = random.randrange(10, 255)


# Color management
colorState = 0
colorStateMax = 4
colorCounter = 1

# brightness management
brightnessState = 0.04
brightnessStateMax = 0.9
brightnessCounter = 0.01
brightConfirm = 0.03

# time management
waitMin = 0.2
waitState = 0.2
waitCounter = 0.2
waitMax = 1
longWaitMax = 15
longWaitState = 0.2

# Set up A1 and A2 as touch inputs
color_A2 = touchio.TouchIn(board.A2)
bright_A1 = touchio.TouchIn(board.A1)

# Number of Blinks
blink = 1
waitTime = 0.1
waitOptTwo = 0.2

# Initialize the onboard NeoPixels
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=brightnessState, auto_write=False)

#####################
##### FUNCTIONS #####
#####################
def confirm(color1, color2, bright, numberBlink, wait):
    for i in range(numberBlink):
        pixels.brightness = bright
        pixels.fill(color1)
        pixels.show()
        time.sleep(wait)
        pixels.fill(color2)
        pixels.show()
        time.sleep(wait)
        

def onlyWhite(bright):
    global WHITE
    pixels.brightness = bright
    pixels.fill(WHITE)
    pixels.show()
    time.sleep(0.2)


def randColors(a, b, c, bright, wait=0.2):
    pixels.brightness = bright
    pixels.fill((a, b, c))
    pixels.show()
    time.sleep(wait)


# COLOR CHASE
def colorChase(color, brightness, wait):
    for i in range(10):
        pixels.brightness = brightness
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)
 
 
# Purple is down, Yellow is up (fixed typo in comment)
def statusColor(color, bright):
    pixels.brightness = bright
    pixels.fill(color)
    pixels.show()
    time.sleep(0.2)


def selectColor(colors, bright):
    pixels.brightness = bright
    pixels.fill(colors)
    pixels.show()
    time.sleep(0.4)


def checkColorIndex():
    global colorIndex
    global colorList 
    global colorListMax
    
    if colorIndex  > colorListMax -1:
        colorIndex = 0
    
while True:

    time.sleep(0.2)
    checkColorIndex()
    
    # if button 1 pressed
    if bright_A1.value:
        confirm(TEAL, OFF, brightConfirm, blink, waitTime)
        print("Brightness: " + str(brightnessState))
        brightnessState = brightnessState + brightnessCounter
        if brightnessState > brightnessStateMax:
            brightnessState = 0.06

    # if button 2 pressed
    elif color_A2.value:
        confirm(RED, OFF, brightConfirm, blink, waitTime)
        print("color state: " + str(colorState))
        print ("blink number:  " + str(blink))
        colorState = colorState + 1
        blink = blink +c1 
        if blink > 5:
            blink = 0
        if colorState > colorStateMax:
            colorState = 0

    if colorState == 0:
        onlyWhite(brightnessState)
        
    elif colorState == 1:
        print("select color")
        checkColorIndex()
        selectColor(colorList[colorIndex], brightnessState)
        if color_A2.value and bright_A1.value:
            confirm(BLUE, ORANGE, brightConfirm, blink, waitOptTwo)
            colorIndex = colorIndex + 1
            print("chose color: " + str(colorIndex))
            checkColorIndex()

    elif colorState == 2:
        print("color Chase Function")
        checkColorIndex()
        colorChase(colorList[colorIndex], brightnessState, waitState)
        colorIndex += 1
        checkColorIndex()
        if color_A2.value and bright_A1.value:
            confirm(BLUE, ORANGE, brightConfirm, blink, waitOptTwo)
            print("wait time: " + str(waitState))
            waitState = waitState + waitCounter
            if waitState > waitMax:
                waitState = waitMin
    
    elif colorState == 3:
        time.sleep(0.7)
        print("Random Color: " + str(r) + ", " + str(g) + ", " + str(b))
        randColors(r, g, b, brightnessState)
        if color_A2.value and bright_A1.value:
            confirm(BLUE, ORANGE, brightConfirm, blink, waitOptTwo)
            r = random.randrange(10, 255)
            g = random.randrange(10, 255)
            b = random.randrange(10, 255)

    
    elif colorState == 4:  # This is just an example condition
        print("Status Color change")
        statusColor(colorList[colorIndex], brightnessState)
        colorIndex = colorIndex + 1
        time.sleep(longWaitState)
        if color_A2.value and bright_A1.value:
            confirm(BLUE, ORANGE, brightConfirm, blink, waitOptTwo)
            print("long wait state: " + str(longWaitState))
            longWaitState = longWaitState * 1.5
            if longWaitState > longWaitMax:
                longWaitState = waitMin
    
    elif colorState == 5:
        print("Single Color")
        checkColorIndex
        statusColor(colorList[colorIndex], brightnessState)
        if color_A2.value and bright_A1.value:
            confirm(PURPLE, YELLOW, brightConfirm, blink, waitOptTwo)
            time.sleep(0.5)
            print("Color: " + str(colorList[colorIndex]))
            print("color index: " + str(colorIndex))
            colorIndex = colorIndex + 1
            checkColorIndex()
            
