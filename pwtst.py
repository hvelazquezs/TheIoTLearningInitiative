import mraa 
import time 

 
x = mraa.Pwm(3) 
x.period_us(1) 
x.enable(True)
x.write(0.5)
x.read() 
value= 0.0 

 
while True: 
   x.write(value) 
   time.sleep(0.05) 
   value = value + 0.01
   print(value)  
   time.sleep(1)
   if value >= 1: 
      value = 0.0
