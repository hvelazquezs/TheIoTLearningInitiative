"""
PrFinal00.py
This example capture the values of the voltage in ADC0 (analogue 0) and 
the current value in ADC1 (analogue 1) 
Makes a port 5 as pwm controlled by mqtt command and execute and zero cross
in the digital port 2 to sync the pwm in the port 5
tIt uses the Python programming language, The groove button as sync zero cross,
the groove potentiometer as voltage input, any groove sensor as current input,
the groove led indicator as pwm output
and the MRAA library.

All this components can be substituted by an isolated mosfet as pwm output, 
one isolated zero cross detector to sync the pwm output, one voltage and 
current detectors as ADC0 and ADC1 inputs, and only adjust the 
equivalences of voltage and current in this code....

The final propose is the full control and monitoring of any load in an alternating 
current home grid remotely by mqtt protocol (can use any communication protocol)...

This is an example code is in the public domain.

Revision History
------------------------------------------------
Author		    	  Date		     	  Description
------------------------------------------------
Hector Velazquez			8-20-2016		Example created
"""


import mraa 
import time 
import pyupm_grove as grove 
import datetime as dt
import paho.mqtt.client as paho
import psutil
import signal
import sys
import time
from threading import Thread

button = grove.GroveButton(2)


n1=dt.datetime.now()
n2=dt.datetime.now()


def SyncSignal(PwPercent):   #wait for a change a signal and capture time betwin two signals
   while (button.value()==0):
      print button.name(), ' value is ', button.value()
      #time.sleep(1)
      n1=dt.datetime.now()
   else:
      n2=dt.datetime.now()

   TimeButton=(n2-n1).microseconds/1e6
   tx0=1/TimeButton
   print TimeButton
   print (button.value())
   print tx0
   x = mraa.Pwm(3)
   x.period_us(TimeButton)
   x.enable(True)
   x.write(PwPercent)
   x.read()
   pass
   
def FullControl(mosq, obj, msg):   #Mqtt execute command
   print "MQTT dataMessageHandler %s %s" % (msg.topic, msg.payload)
    
   if (msg.payload=="off" or msg.payload=="Off" or msg.payload=="OFF"):
      x = mraa.Pwm(3)
      x.enable(False)
      x.write(0.0)
      #SyncSignal(0.0)
      #return			   
   
   elif (msg.payload=="on" or msg.payload=="ON" or msg.payload=="On"):
      x = mraa.Pwm(3)
      x.enable(True)
      SyncSignal(1.0)
      #return			   
	  
   elif (msg.payload=="%"):
      PtValue = msg.payload[1:2]
      PwValue = PtValue/100
      SyncSignal(PwValue)
      #return
			   
   elif (msg.payload=="break" or msg.payload=="Break"):
      print "Program terminated by remote user..."
      SyncSignal(0)
      os._exit(1)
   else:
      print "write only 'on' or 'off' or break to terminate..."
   
def on_publish(mosq, obj, msg):
    pass

def dataVolt(): # Get Voltage and current data
   xpt=0.0
   try:
      xpi= mraa.Aio(0)
      for i in range (25):
         xp = xpi.readFloat()  #(xp + xpi.readFloat())
         xpt=xp+xpt
         print xp
         print xpt
      xv=xpt / 25
      print ('The current value is= ', xv)
   except:
      print ("Error capturing the Voltage(V) value data...")
   return xv
   
def dataAmps():
   xpt=0.0
   try:
      xpi= mraa.Aio(1)
      for i in range (25):
         xp = xpi.readFloat()  #(xp + xpi.readFloat())
         xpt=xp+xpt
         print xp
         print xpt
      xi=xpt / 25
      print ('The current value is= ', xi)
   except:
      print ("Error capturing the current(i) value data...") 
   return xi

def dataNetworkHandler(): #Mqtt publish data (Voltage, current and Percent of load)
   idVolts = "VoltageDevice"
   idAmps = "Currentdevice"
   idPercent = "%00"
   mqttclient = paho.Client()
   mqttclient.on_publish = on_publish
   mqttclient.connect("test.mosquitto.org", 1883, 60)
   while True:
      message1 = idVolts + " " + str(dataVolt())
      message2 = idAmps + " " + str(dataAmps())
      message3 = idPercent + " " + str(PwPercent)
      mqttclient.publish("IoT101/Volts", message1)
      mqttclient.publish("IoT101/Amps", message2)
      mqttclient.publish("IoT101/Percent", message3)
      time.sleep(1)
		
def on_message(mosq, obj, msg):
    print "MQTT dataMessageHandler %s %s" % (msg.topic, msg.payload)

def dataMessageHandler():
   mqttclient = paho.Client()
   mqttclient.on_message = on_message
   mqttclient.connect("test.mosquitto.org", 1883, 60)
   mqttclient.subscribe("IoT101/Voltage", 0)
   mqttclient.subscribe("IoT101/Current", 0)
   mqttclient.subscribe("IoT101/Percent", 0)
   while mqttclient.loop() == 0:
      pass

if __name__ == '__main__':
   #Main program
   threadx = Thread(target=dataNetworkHandler)
   threadx.start()
   threadx = Thread(target=dataMessageHandler)
   threadx.start()
 