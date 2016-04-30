#!/usr/bin/python
import pyupm_i2clcd as lcd 
import psutil
import pywapi
import signal
import sys
import time
import paho.mqtt.client as paho
import string
#import ploty.ploty as py
#from plotly.graph_objs import Scatter, Layout, Figure


from threading import Thread
from flask import Flask
from flask_restful import Api, Resource

#username = 'TheIoTLearningInitiative'
#api_key = 'twr0hlw78c'
#stream_token = '2v04m1lk1x'

#p=0
#stream = py.Stream(stream_token)
idDevice = "IoT101Device"
message = ""
data={}


myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62) 
myLcd.setCursor(0,0) 
myLcd.setColor(255,0,0)
myLcd.setCursor(0,0) 
myLcd.write('Initialized...')
myLcd.setCursor(1,0) 
myLcd.write('Please Wait . . .') 
app=Flask(__name__)
api=Api(app)

def GetMACAdress():
	gtMAC=open('/sys/class/net/wlan0/address').read()
	return gtMAC[0:17]

def interruptHandler(signal, frame):
		sys.exit(0)

def on_publish(mosq, obj, msg):
		pass

def dataNetwork():
    		netdata = psutil.net_io_counters()
    		return netdata.packets_sent + netdata.packets_recv

def dataNetworkHandler():
               	i=0
		a=0
		b=15
		#mqttclient = paho.Client()
		#mqttclient.on_publish = on_publish
		#mqttclient.connect("test.mosquitto.org", 1883, 60)
		while True:
			#stream_data = dataPlotly()
			#stream.write({'x': i, 'y': stream_data})
			#p += 1
			LcdShow=""
			print "Hello Internet of Things 101"
			idDevice=GetMACAdress()		
                        myLcd.setColor(53, 39, 249)
                        packets = dataNetwork()
                        message = idDevice + " " + str(packets)
			print "dataNetworkHandler " + message
			#mqttclient.publish("IoT101/Network", data)
			LcdShow=('MAC: '+idDevice)
			myLcd.setCursor(1,7) 
			myLcd.write(' CPU% '+str(psutil.cpu_percent()))
			myLcd.setCursor(0,0) 
			myLcd.write(LcdShow[a:b]) 
			myLcd.setCursor(1,0)
			myLcd.write('Pk:' + str(packets))
			data[i]=message
			a=a+1
			b=b+1
			i=i+1
			if (b>=23):
				a=0
				b=15
			
			if (i==16):
				i=0
		
			
			time.sleep(2)
			

class Network(Resource):
	def get(self):
		return(data)

 
if __name__ == '__main__':

	
	signal.signal(signal.SIGINT, interruptHandler)

    	threadx = Thread(target=dataNetworkHandler)
    	
	threadx.start()

#	thready = Thread(target=dataMessageHandler)
#	thready.start()
#	threadz = Thread(target=dataPlotlyHandler)
#	threadz.start()

    	while True:
        	print "Hello Internet of Things 101"
		api.add_resource(Network,'/network')
		app.run(host='0.0.0.0',debug=True) 
		#dataWeatherHandler()		
		time.sleep(3)
	

# End of File

