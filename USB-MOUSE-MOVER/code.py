# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import busio
import board
import digitalio
import usb_hid
import terminalio
import displayio
import microcontroller
from adafruit_display_text import label
from adafruit_st7789 import ST7789
from time import sleep
from adafruit_hid.mouse import Mouse

# First set some parameters used for shapes and text
BORDER = 10
FONTSCALE = 4
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00

mouse = Mouse(usb_hid.Device.MOUSE)

# Release any resources currently in use for the displays
displayio.release_displays()
spi = busio.SPI(clock=board.GP18,MOSI=board.GP19)
tft_cs = board.GP17
tft_dc = board.GP16
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53)

led = digitalio.DigitalInOut(board.GP7)
led.direction = digitalio.Direction.OUTPUT

button_x = digitalio.DigitalInOut(board.GP14)
button_x.direction = digitalio.Direction.INPUT
button_x.pull = digitalio.Pull.UP

button = True
counter = int(0)

def DispPrint(text):
    # Make the display context
    splash = displayio.Group()
    display.show(splash)

    # Draw a label
    display.show(splash)
    text_area = label.Label(terminalio.FONT, text=text, color=TEXT_COLOR)
    text_width = text_area.bounding_box[2] * FONTSCALE
    text_group = displayio.Group(
        scale=FONTSCALE,
        x=display.width // 2 - text_width // 2,
        y=display.height // 2,
    )
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)



def MySleep(sleeptime):
    sleepval = 0.1
    sleepcur = 0
    while ( sleepcur < sleeptime and button_x.value is True ) :
        sleepcur = sleepcur + sleepval
        sleep(sleepval)


while button:
    counter = counter + 1
    DispPrint('' + str(counter))
    button = button_x.value
    led.value = False
    try:
        mouse.move(x=10)
        mouse.move(x=-10)
    except:
        DispPrint('Error')
        sleep(10)
        import microcontroller
        microcontroller.reset()

    sleep(.2)
    led.value = True
    MySleep(10)

DispPrint('Resetting')
sleep(10)
microcontroller.reset()
