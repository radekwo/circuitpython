
import board
import digitalio


print('Starting boot.py')

led = digitalio.DigitalInOut(board.GP8)
led.direction = digitalio.Direction.OUTPUT
led.value = True

button_x = digitalio.DigitalInOut(board.GP14)
button_x.direction = digitalio.Direction.INPUT
button_x.pull = digitalio.Pull.UP

if button_x.value:
    print('Button X not pressed')
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
    print('Button X is pressed')
    # normal work

led.value = False
print('boot.py done')

