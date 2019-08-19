import cv2
import time
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

cv2_cam = cv2.VideoCapture(1)
time.sleep(2)
t_end = time.time() + 5
while time.time() < t_end:
	print time.time()
	title = 'image' + datetime.now().strftime("%d%m%Y_%H:%M:%S.%f") + '.jpg'
	ret, img = cv2_cam.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite(title, gray)
	time.sleep(0.2)
cv2.destroyAllWindows()
