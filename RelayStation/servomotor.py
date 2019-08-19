import RPi.GPIO as GPIO
import time
import sys, tty, termios

actuatorIN = 27
actuatorOUT = 18
servoPIN = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(actuatorIN, GPIO.OUT, initial = 1)
GPIO.setup(actuatorOUT, GPIO.OUT, initial = 1)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50 Hz
p.start(2.5) # Inititalization

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

try:
	time.sleep(0.5)
	p.ChangeDutyCycle(0)
	while True:
		char = getch()
		if(char == "o"):
			time.sleep(0.5)
			GPIO.output(actuatorOUT, 0)
			time.sleep(62)
			GPIO.output(actuatorOUT, 1)
			p.ChangeDutyCycle(4.7)
			time.sleep(1)
			p.ChangeDutyCycle(0)
			GPIO.output(actuatorIN, 0)
			time.sleep(63)
			GPIO.output(actuatorIN, 1)
		if(char == "c"):
			p.ChangeDutyCycle(2.5)
		        time.sleep(2.5)
			p.ChangeDutyCycle(0)
		if(char == "x"):
			print("Program Ended")
			break
except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
