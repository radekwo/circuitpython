import busio
import board
import digitalio
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_st7789 import ST7789
from time import sleep

# First set some parameters used for shapes and text
BORDER = 10
BACKGROUND_COLOR = 0x00FF00  # Bright Green
FOREGROUND_COLOR = 0xAA0088  # Purple
TEXT_COLOR = 0xFFFF00


# Release any resources currently in use for the displays
displayio.release_displays()
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
tft_cs = board.GP17
tft_dc = board.GP16
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789( display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53 )

led = digitalio.DigitalInOut(board.GP8)
led.direction = digitalio.Direction.OUTPUT
led.value = True

button_x = digitalio.DigitalInOut(board.GP14)
button_x.direction = digitalio.Direction.INPUT
button_x.pull = digitalio.Pull.UP

def DispPrint(text, FONTSCALE = 2):
    # Make the display context
    splash = displayio.Group()
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
    print(text)

DispPrint('Starting boot.py',FONTSCALE=3)

if button_x.value:
    DispPrint('Button X not pressed',FONTSCALE=2)
    # button X not pressed - normal work
    import storage
    import usb_cdc
    import usb_midi
    import usb_hid

    usb_hid.disable()                           # Disable all HID devices.
    usb_hid.enable((usb_hid.Device.MOUSE,))     # Enable only mouse
    storage.disable_usb_drive()  # disable CIRCUITPY
    usb_cdc.disable()            # disable REPL
    usb_midi.disable()           # disable MIDI
else:
    DispPrint('Button X is pressed',FONTSCALE=2)
    # normal work
led.value = False
DispPrint('boot.py done')
sleep(5)
