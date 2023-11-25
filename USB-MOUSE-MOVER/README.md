**small project to emulate USB mouse moves on screen for disable screen-lock**
- when X button is pressed while boot - board dont hide usb-storage and other usb devices ( possible edit files with Mu editor )
- when X button is NOT pressed while boot - board hide usb-storage devices, only mouse is visible
- when X button is pressed while work - board restarts
- when board works, green led blinking and LCD display counter with number of mouse move actions

to run:
- flash PI with u2f circuitpython image
- after reboot extract to directory */lib*
  - *adafruit_hid* folder from adafruit-circuitpython-hid-7.x-mpy-5.2.1.zip
  - *adafruit_bus_device* folder from adafruit-circuitpython-bundle-7.x-mpy-20220119.zip
  - *adafruit_display_text* folder from  adafruit-circuitpython-bundle-7.x-mpy-20220119.zip
  - *adfruit_st7789.mpy* file from adafruit-circuitpython-bundle-7.x-mpy-20220119.zip
- copy to */* directory files:
  - *boot.py*
  - *code.py*
