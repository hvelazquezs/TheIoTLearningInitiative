import time 
import pyupm_grove as grove 
import datetime as dt
n1=dt.datetime.now()
n2=dt.datetime.now()

# Create the button object using GPIO pin 0 
button = grove.GroveButton(2)
 

# Read the input and print, waiting one second between readings 
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
