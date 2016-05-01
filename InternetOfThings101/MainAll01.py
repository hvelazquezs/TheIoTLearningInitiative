#!/usr/bin/python
import pyupm_i2clcd as lcd 
import psutil
import pywapi
import signal
import os
import sys
import time
import paho.mqtt.client as paho
import string
import plotly.plotly as py
import dweepy
import pyupm_grove as grove
from plotly.graph_objs import Scatter, Layout, Figure
from threading import Thread
from flask import Flask
from flask_restful import Api, Resource

username = 'hvelazquezs'
api_key = 's2s780r8rl'
stream_token = '09wwi43qla'

bar0="**************************************************************"
bar1="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
bar2="=============================================================="

relay1=grove.GroveRelay(2)

p=0
stream = py.Stream(stream_token)
idDevice = "None"
message = "Empty message..."
data={}

myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62) 
myLcd.setCursor(0,0) 
myLcd.setColor(255,0,0)
myLcd.setCursor(0,0) 
myLcd.write('  Starting...')
myLcd.setCursor(1,0) 
myLcd.write('  Please Wait...') 
app=Flask(__name__)
api=Api(app)


def GetMACAdress():
	gtMAC=open('/sys/class/net/wlan0/address').read()
	return gtMAC[0:17]

def interruptHandler(signal, frame):
		sys.exit(0)

def on_publish(mosq, obj, msg):
    pass

def on_Port2(mosq, obj, msg):
    print "MQTT dataMessageHandler %s %s" % (msg.topic, msg.payload)
    
    if (msg.payload=="off" or msg.payload=="Off" or msg.payload=="OFF"):
               relay1.off()
               print "Relay is off..."
               myLcd.setColor(255, 32, 0)
    
    elif (msg.payload=="on" or msg.payload=="ON" or msg.payload=="On"):
               relay1.on()
               print "Relay is on..."
               myLcd.setColor(0, 255, 0)

    elif (msg.payload=="break" or msg.payload=="Break"):
           print "Program terminated by remote user..."
           relay1.off()
           myLcd.setColor(255,0,0)
           myLcd.setCursor(0,0) 
           myLcd.write('                ') 
           myLcd.setCursor(1,0) 
           myLcd.write('                ') 
           myLcd.setColor(0,0,0)
           os._exit(1)
    else:
           print "write only 'on' or 'off' or break to terminate..."

def dataMessageHandler():
    idDevice=GetMACAdress()
    mqttclient = paho.Client()
    mqttclient.on_message = on_Port2
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    mqttclient.subscribe("IoT101/" + idDevice + "/Port2", 0)
    while mqttclient.loop() == 0:
        pass


def dataNetwork():
    		netdata = psutil.net_io_counters()
    		return netdata.packets_sent + netdata.packets_recv

def dataNetworkHandler():
               	i=0
		a=0
		b=15
		mqttclient = paho.Client()
		mqttclient.on_publish = on_publish
		mqttclient.connect("test.mosquitto.org", 1883, 60)
		while True:
			dataWeatherHandler()
			LcdShow="              "
			print bar0
			idDevice=GetMACAdress()		
                        myLcd.setColor(53, 39, 249)
                        packets = dataNetwork()
                        message = idDevice + " " + str(packets)
			print "dataNetworkHandler " + message
			print "MQTT dataNetworkHandler " + message
			mqttmsg = "IoT101/" + idDevice + "/Network"
			mqttclient.publish(mqttmsg, message)
			pass0={'network':packets}
			dweepy.dweet_for('hvelazquezs',pass0)
			LcdShow=('MAC: '+ idDevice)
			myLcd.setCursor(1,8) 
			myLcd.write(' CPU%'+str(psutil.cpu_percent()))
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
			
    
def dataWeatherHandler():
    weather = pywapi.get_weather_from_weather_com('MXJO0043', 'metric')
    msg1 = "Weather.com report in " 
    msg2 = ",Temperature "
    msg3 = weather['current_conditions']['temperature']+" C"
    msg4 = ", Atmospheric Pressure "
    msg5 = weather['current_conditions']['barometer']['reading'][:-3]
    msg6 = " mbar"
    print msg1+msg2+msg3+msg4+msg5+msg6


def dataPlotly():
    return dataNetwork()

def dataPlotlyHandler():
    
    py.sign_in(username, api_key)

    trace1 = Scatter(
        x=[],
        y=[],
        stream=dict(
            token=stream_token,
            maxpoints=200
        )
    )

    layout = Layout(
        title='Hello Internet of Things 101 Data'
    )

    fig = Figure(data=[trace1], layout=layout)

    print py.plot(fig, filename='Hello Internet of Things 101 Plotly')

    i = 0
    stream = py.Stream(stream_token)
    stream.open()

    while i < 99:
        stream_data = dataPlotly()
        stream.write({'x': i, 'y': stream_data})
        i += 1
        time.sleep(0.25)


class Network(Resource):
	def get(self):
		return(data)

 
if __name__ == '__main__':

	
	signal.signal(signal.SIGINT, interruptHandler)


   	threadx = Thread(target=dataNetworkHandler)
    	threadx.start()

    	threadx = Thread(target=dataMessageHandler)
    	threadx.start()

	threadz = Thread(target=dataPlotlyHandler)
	#threadz.start()
   
	while True:		
		print bar1
        	print "Hello Internet of Things 101" 
		api.add_resource(Network, '/network')
		app.run(host='0.0.0.0', debug=True)		
		time.sleep(5)

# End of File



