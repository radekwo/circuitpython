
import busio
import board
import digitalio
import usb_hid
import supervisor
import microcontroller
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_st7789 import ST7789
from time import sleep
from adafruit_hid.mouse import Mouse



print('code.py stsarted')

# Release any resources currently in use for the displays
displayio.release_displays()
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
tft_cs = board.GP17
tft_dc = board.GP16
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53
)

ledR = digitalio.DigitalInOut(board.GP6)
ledR.direction = digitalio.Direction.OUTPUT
ledR.value = True  # led is OFF
ledG = digitalio.DigitalInOut(board.GP7)
ledG.direction = digitalio.Direction.OUTPUT
ledG.value = True  # led is OFF
ledB = digitalio.DigitalInOut(board.GP8)
ledB.direction = digitalio.Direction.OUTPUT
ledB.value = True  # led is OFF

button_y = digitalio.DigitalInOut(board.GP15)
button_y.direction = digitalio.Direction.INPUT
button_y.pull = digitalio.Pull.UP

button = True
counter = int(0)

# First set some parameters used for shapes and text
BORDER = 10
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00

def DispPrint(text, FONTSCALE = 2):
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
    while sleepcur < sleeptime and button_y.value is True:
        sleepcur = sleepcur + sleepval
        sleep(sleepval)


def reset():
    microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
    microcontroller.reset()
    
try:
    mouse = Mouse(usb_hid.Device.MOUSE)
except:
    DispPrint("Error mouse init",FONTSCALE=2)
    sleep(10)
    reset()
    
while button:
    counter +=1
    DispPrint("" + str(counter),FONTSCALE=4)
    button = button_y.value
    ledG.value = False  # led is ON
    try:
        mouse.move(x=10)
        mouse.move(x=-10)
    except:
        ledG.value = True  # led is OFF
        ledR.value = False # led is ON
        DispPrint("mouse move Error")
        sleep(10)
        reset()
    sleep(0.2)
    ledG.value = True
    MySleep(10)

ledB.value = False
DispPrint("Resetting")
sleep(10)
DispPrint("         ")
reset()
