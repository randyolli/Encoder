# Git integrated

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

PIN_CLK = 2
PIN_DAT = 3
PIN_CS  = 4
delay = 0.0000005
ns = 1 # number of sensors attached
callibration = 105
# totally 10 bits to be extracted from SSI signal
bitcount = 16

# pin setup done here
try:
    GPIO.setup(PIN_CLK, GPIO.OUT)
    GPIO.setup(PIN_DAT, GPIO.IN)
    GPIO.setup(PIN_CS, GPIO.OUT)                                                                                                    
    GPIO.output(PIN_CS,1 )
    GPIO.output(PIN_CLK, 1)
except:
    print "ERROR. Unable to setup the configuration requested"                                     

#wait some time to start
time.sleep(0.5)

print "GPIO configuration enabled"

def clockup():
    GPIO.output(PIN_CLK,1)
def clockdown():
    GPIO.output(PIN_CLK,0)
def MSB():
    # Most Significant Bit
    clockdown()

def readpos():
    GPIO.output(PIN_CS,0)
    time.sleep(delay*2)
    MSB()
    data = 0
    
    for i in range(0,bitcount):
        if i<10:
            #print i
            clockup()
            data <<= 1  
            data |= GPIO.input(PIN_DAT)
            clockdown()
        else:
            for k in range(0,6):
                clockup()
                clockdown()
    GPIO.output(PIN_CS,1)
    return data

try:
    while(1):
        x = readpos()
        angle = (x * 360/1024)
        anglec = angle + callibration
        anglec = anglec % 360
        
        # print angle
        print anglec
        time.sleep(0.1)
        #break
        
finally:
    print "cleaning up GPIO"
    GPIO.cleanup()
