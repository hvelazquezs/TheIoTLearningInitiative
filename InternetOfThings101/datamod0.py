#!/usr/bin/python

import psutil
import signal
import sys
import time
import pyupm_i2clcd as lcd

myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
myLcd.setColor(53, 39, 249)
#myLcd.setColor(255, 0, 0)
myLcd.setCursor(0,0)



from threading import Thread

def interruptHandler(signal, frame):
    sys.exit(0)

def dataNetwork():
    netdata = psutil.net_io_counters()
    return netdata.packets_sent + netdata.packets_recv

def dataNetworkHandler():
    idDevice = "IoT101Device"
    while True:
        packets = dataNetwork()
        message = idDevice + " " + str(packets)
        print "dataNetworkHandler " + message
	myLcd.setCursor(0,0)
	myLcd.write(idDevice)
	myLcd.setCursor(1,0)
	myLcd.write(str(packets))

        time.sleep(1)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, interruptHandler)

    threadx = Thread(target=dataNetworkHandler)
    threadx.start()

    while True:
        print "Hello Internet of Things 101"
        time.sleep(5)

# End of File

