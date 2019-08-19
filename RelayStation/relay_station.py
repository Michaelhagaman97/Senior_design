
import RPi.GPIO as GPIO
import time
import sys, tty, termios
import select
import threading
from datetime import datetime
import RPi.GPIO as GPIO
import picamera
import cv2
 
actuatorIN = 27
actuatorOUT = 18
servoPIN = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(actuatorIN, GPIO.OUT, initial = 1)
GPIO.setup(actuatorOUT, GPIO.OUT, initial = 1)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50 Hz
p.start(2.5) # Inititalization


def isData():
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

old_settings = termios.tcgetattr(sys.stdin)

def motor_open():
	print "Opening doors"
	GPIO.output(actuatorOUT, 0)
        time.sleep(62)
        GPIO.output(actuatorOUT, 1)
        p.ChangeDutyCycle(4.7)
        time.sleep(1)
        p.ChangeDutyCycle(0)
        GPIO.output(actuatorIN, 0)
        time.sleep(63)
        GPIO.output(actuatorIN, 1)
	print "Doors open"

def motor_close():
	print "Closing doors"
	p.ChangeDutyCycle(2.5)
        time.sleep(1)
        p.ChangeDutyCycle(0)
	print "Doors closed"

with picamera.PiCamera() as camera:
	camera.resolution = (640,480)
	camera.framerate = 5
	camera.iso = 800
	try:
		time.sleep(1)
		p.ChangeDutyCycle(0)
		day_night = 0
	        day_cam = 0
		night_cam = 0        
	        while True:
			pirsensor = GPIO.input(4)
	                if day_cam == 1:
				print "Day cam start"
				camera.start_preview()
	                        time.sleep(2)
	                        while day_cam == 1:
					title = 'image' +datetime.now().strftime("%d%m%Y_%H:%M:%S.%f")
					camera.capture(title, format='jpeg', use_video_port=True)
					if isData():
						c = sys.stdin.read(1)
						if c == 'n':
							day_cam = 0
							night_cam = 1
						if c == 's':
							day_cam = 0
							night_cam = 0
							print "Recording stopped"
	                			if c == 'o':
			                                if threading.active_count() < 2:
			                                        t1 = threading.Thread(target=motor_open)
			                                        t1.start()
			                                else:
			                                        print "Threads busy"
			                        if c == 'c':
			                                if threading.active_count() < 2:
			                                        t2 = threading.Thread(target=motor_close)
			                                        t2.start()
			                                else:
			                                        print "Threads busy"
				camera.stop_preview()
				print "Day cam off"
			elif night_cam == 1:
	                        print "Night cam start"
				cv2_cam = cv2.VideoCapture(1)
	                        time.sleep(2)
				while night_cam == 1:
					title = 'image' + datetime.now().strftime("%d%m%Y_%H:%M:%S.%f") + '.jpg'
				        ret, img = cv2_cam.read()
				        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
				        cv2.imwrite(title, img)
				        time.sleep(0.2)
					if isData():
	                                        c = sys.stdin.read(1)
	                                        if c == 'd':
	                                                day_cam = 1
	                                                night_cam = 0
	                                        if c == 's':
	                                                day_cam = 0
	                                                night_cam = 0
	                                                print "Recording stopped"
						if c == 'o':
			                                if threading.active_count() < 2:
			                                        t1 = threading.Thread(target=motor_open)
			                                        t1.start()
			                                else:
			                                        print "Threads busy"
			                        if c == 'c':
			                                if threading.active_count() < 2:
			                                        t2 = threading.Thread(target=motor_close)
			                                        t2.start()
			                                else:
			                                        print "Threads busy"
				#cv2.destroyAllWindows()
				print "Night cam off"
	              	elif pirsensor == 1:
				if day_night == 0:
					print "Day camera motion start"
					camera.start_preview
					time.sleep(2)
					while pirsensor == 1 and day_cam == 0 and night_cam == 0:
						title = 'image' + datetime.now().strftime("%d%m%Y_%H:%M:%S.%f")
			                        camera.capture(title, format='jpeg', use_video_port=True)
						pirsensor = GPIO.input(4)
						if isData():
					                c = sys.stdin.read(1)
					                if c == 'd':
					                        day_cam = 1
					                        night_cam = 0
					                if c == 'n':
					                        day_cam = 0
					                        night_cam = 1
					                if c == 's':
					                        day_cam = 0
					                        night_cam = 0
					                        print "Recording stopped"
					                if c == 'o':
					                        if threading.active_count() < 2:
					                                t1 = threading.Thread(target=motor_open)
					                                t1.start()
					                        else:
					                                print "Threads busy"
					                if c == 'c':
					                        if threading.active_count() < 2:
					                                t2 = threading.Thread(target=motor_close)
					                                t2.start()
					                        else:
					                                print "Threads busy"
					camera.stop_preview()
					print "Day camera motion off"
				else:
					print "Night camera motion start"
					cv2_cam = cv2.VideoCapture(1)
					time.sleep(2)
					while pirsensor == 1 and day_cam == 0 and night_cam == 0:
						pirsensor = GPIO.input(4)
						title = 'image' + datetime.now().strftime("%d%m%Y_%H:%M:%S.%f") + '.jpg'
					        ret, img = cv2_cam.read()
					        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					        cv2.imwrite(title, img)
					        time.sleep(0.2)
						if isData():
	                                                c = sys.stdin.read(1)
	                                                if c == 'd':
	                                                        day_cam = 1
	                                                        night_cam = 0
	                                                if c == 'n':
	                                                        day_cam = 0
	                                                        night_cam = 1
	                                                if c == 's':
	                                                        day_cam = 0
	                                                        night_cam = 0
	                                                        print "Recording stopped"
	                                                if c == 'o':
	                                                        if threading.active_count() < 2:
	                                                                t1 = threading.Thread(target=motor_open)
	                                                                t1.start()
	                                                        else:
	                                                                print "Threads busy"
	                                                if c == 'c':
	                                                        if threading.active_count() < 2:
	                                                                t2 = threading.Thread(target=motor_close)
	                                                                t2.start()
	                                                        else:
	                                                                print "Threads busy"
					#cv2.destroyAllWindow()
					print "Night camera motion off"
			else:
				if isData():
	                                c = sys.stdin.read(1)
	                                if c == 'n':
	                         	        day_cam = 0
	                             		night_cam = 1
					if c == 'd':
	                                        day_cam = 1 
	                                        night_cam = 0
					if c == 'x':
						print "Program ended"
						break
					if c == 'o':
		                                if threading.active_count() < 2:
		                                        t1 = threading.Thread(target=motor_open)
		                                        t1.start()
		                                else:
		                                        print "Threads busy"
		                        if c == 'c':
		                                if threading.active_count() < 2:
		                                        t2 = threading.Thread(target=motor_close)
		                                        t2.start()
		                                else:
		                                        print "Threads busy"
					if c == '1':
						day_night = 0
						print "Daytime selected"
					if c == '2':
						day_night = 1
						print "Nighttime selected"
	finally:
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
		p.stop()
		GPIO.cleanup()
