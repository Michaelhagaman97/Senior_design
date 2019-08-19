import time
import picamera
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

with picamera.PiCamera() as camera:
	camera.resolution = (640,480)
	camera.framerate = 5
	camera.iso = 800
	camera.start_preview()
	try:
		time.sleep(2)
		t_end = time.time() + 5
		while time.time() < t_end:
			title = 'image' + datetime.now().strftime("%d%m%Y_%H:%M:%S.%f")
			camera.capture(title, format='jpeg', use_video_port=True)
	finally:
		camera.stop_preview()
