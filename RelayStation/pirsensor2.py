import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

while True:
	i = GPIO.input(4)
	if i==0:
		print "No movement", i 
	if i==1:
		print "Movement:", i
	time.sleep(2.5)
