#!/usr/bin/python
import pyupm_i2clcd as lcd 
import psutil
import pywapi
import signal
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
relay2=grove.GroveRelay(3)


p=0
stream = py.Stream(stream_token)
idDevice = "No MAC Get it..."
message = "Empty message..."
data={}


myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62) 
myLcd.setCursor(0,0) 
myLcd.setColor(255,0,0)
myLcd.setCursor(0,0) 
myLcd.write('   Initialized...')
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

def dataNetwork():
    		netdata = psutil.net_io_counters()
    		return netdata.packets_sent + netdata.packets_recv

def dataNetworkHandler():
               	i=0
		a=0
		b=15
		mqttclient = paho.Client()
		mqttclient.on_publish = on_publish
		mqttclient.on_message = onRelay
		mqttclient.connect("test.mosquitto.org", 1883, 60)
		while True:
			dataWeatherHandler()
			#dataMessageHandler()
			LcdShow="              "
			print bar0
			print "Hello Internet of Things 101"
			idDevice=GetMACAdress()		
                        myLcd.setColor(53, 39, 249)
                        packets = dataNetwork()
                        message = idDevice + " " + str(packets)
			print "dataNetworkHandler " + message
			print "MQTT dataNetworkHandler " + message
			pass0={'network':packets}
			dweepy.dweet_for('hvelazquezs',pass0)
			mqttmsg="IoT101/"+idDevice+"/Network"
			mqttclient.publish(mqttmsg,message)
			mqttmsk="IoT101/"+idDevice+"/Relay"
			mqttclient.subscribe(mqttmsk,1)
			print mqttmsk
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
		
			#dataMessageHandler()
			time.sleep(1)
			

class Network(Resource):
	def get(self):
		return(data)

def onRelay():
    relay1.on()
    relay2.on()
    myLcd.setColor(255, 0, 0)
    print "Relay is on..."
    time.sleep(5)
    relay1.off()
    relay2.off()
    myLcd.setColor(0, 255, 0)
    print "Relay is off..."
       
    
def dataMessageHandler():
    mqttclient = paho.Client()
    mqttclient.on_message = onRelay()
    mqttclient.connect("test.mosquitto.org", 1883, 60)
    mqttclient.subscribe("IoT101/"+idDevice+"/Port2", 0)
    #mqttclient.on_message = onRelay()
    myLcd.setColor(0, 0, 255)
    while mqttclient.loop() == 0:
        pass

def dataWeatherHandler():
    weather = pywapi.get_weather_from_weather_com('MXJO0043', 'metric')
    msg1 = "Weather.com report in " 
    #+ weather['location']['city']
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



 
if __name__ == '__main__':

	
	signal.signal(signal.SIGINT, interruptHandler)

	thready = Thread(target=dataMessageHandler)
	thready.start()
	threadx = Thread(target=dataNetworkHandler)
    	threadx.start()
	#threadz = Thread(target=dataPlotlyHandler)
	#threadz.start()
   
	#while True:		
	#	print bar1
        #	print "Hello Internet of Things 101" 
		#api.add_resource(Network, '/network')
		#app.run(host='0.0.0.0', debug=True)		
	#	time.sleep(5)

# End of File



