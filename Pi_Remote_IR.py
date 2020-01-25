import RPi.GPIO as GPIO
import IRModule
import time
from lib_oled96 import ssd1306
from smbus import SMBus

GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(17, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
i2cbus = SMBus(1) 
oled = ssd1306(i2cbus)
draw = oled.canvas

oled.cls()
oled.display()

current_milli_time = lambda: int(round(time.time() * 1000))
def reset_LEDs():
  GPIO.output(17, 0)
  GPIO.output(27, 0)
  GPIO.output(22, 0)
  oled.cls()
  return

def remote_callback(code):
    if code == 16738455: #Button 0
      reset_LEDs()
      GPIO.output(17, 1)
      draw.text((20, 16), "Button 0", fill=1)

    if code == 16724175: #Button 1
      reset_LEDs()
      GPIO.output(27, 1)
      draw.text((20, 16), "Button 1", fill=1)

    if code == 16718055: #Button 2
      reset_LEDs()
      GPIO.output(22, 1)
      draw.text((20, 16), "Button 2", fill=1)

    oled.display()

    print(str(code))
    return

irPin = 16
ir = IRModule.IRRemote(callback='DECODE')    
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)      # uses numbering outside circles
GPIO.setup(irPin,GPIO.IN)   # set irPin to input
GPIO.add_event_detect(irPin,GPIO.BOTH,callback=ir.pWidth)

try:    
    ir.set_callback(remote_callback)

    while True:
        time.sleep(1)

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    print('Removing callback and cleaning up GPIO')
    ir.remove_callback()
    GPIO.cleanup()

