import cv2
import numpy as np
from picamera2 import Picamera2
import RPi.GPIO as GPIO

# DEL tricolore
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)	# Rouge
GPIO.setup(15, GPIO.OUT)	# Verte
GPIO.setup(18, GPIO.OUT)	# Bleue

#cap=cv2.VideoCapture(0)
lower_range_green = np.array([46, 61, 45])
upper_range_green = np.array([79, 255, 255])

lower_range_orange = np.array([0, 122, 86])
upper_range_orange = np.array([11, 255, 254])

lower_range_red = np.array([134, 197, 174])
upper_range_red = np.array([179, 255, 255])

lower_range_blue = np.array([85, 183, 82])
upper_range_blue = np.array([126, 255, 255])

lower_range_brown = np.array([144, 0, 0])
upper_range_brown = np.array([179, 253, 123])

lower_range_yellow = np.array([17, 167, 81])
upper_range_yellow = np.array([38, 255, 252])

GPIO.output(14, GPIO.HIGH)
GPIO.output(15, GPIO.HIGH)
GPIO.output(18, GPIO.HIGH)
#GPIO.output(14, GPIO.LOW)
#GPIO.output(15, GPIO.LOW)
#GPIO.output(18, GPIO.LOW)

picam = Picamera2()
#picam.preview_configuration.main.size = (640, 480)
picam.preview_configuration.main.size = (1280, 960)
picam.preview_configuration.main.format = "RGB888"

picam.preview_configuration.align()
picam.configure("preview")
picam.start()
frame = picam.capture_array()

def track(img, lower_range, upper_range, rect_color, nom):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_range, upper_range)
    _, mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    cnts, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    nombre_rectangles = []
    for c in cnts:
        x = 5000
        if cv2.contourArea(c) > x:
            print(cv2.contourArea(c))
            x, y, w, h = cv2.boundingRect(c)
            nombre_rectangles.append(x)
            x1 = int(x + x + w)//2
            y1 = int(y + y + h)//2
            cv2.circle(img, (x1, y1), 4, (255, 0, 255), -1)	# -1 pour remplir
            cv2.rectangle(frame, (x, y), (x+w, y+h), rect_color, 2)
            cv2.putText(frame, (nom), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, rect_color, 2)
            #print("Nombre de M&Ms detectés :", len(nombre_rectangles))
            #cv2.imshow("Masque", mask1)

while True:
    # ret,frame=cap.read()
    frame = picam.capture_array()
    frame = cv2.resize(frame, (640, 480))
    track(frame, lower_range_green, upper_range_green, (0, 255, 0), "Vert")
    track(frame, lower_range_red, upper_range_red, (0, 0, 255), "Rouge")
    track(frame, lower_range_yellow, upper_range_yellow, (0, 255, 255), "Jaune")
    track(frame, lower_range_orange, upper_range_orange, (0, 200, 255), "Orange")
    track(frame, lower_range_brown, upper_range_brown, (40, 40, 140), "Marron")
    track(frame, lower_range_blue, upper_range_blue, (255, 0, 0), "Bleu")
            
    cv2.imshow("FRAME", frame)
    
    if cv2.waitKey(1)&0xFF == 27:
        break
    
GPIO.output(14, GPIO.LOW)
GPIO.output(15, GPIO.LOW)
GPIO.output(18, GPIO.LOW)

GPIO.cleanup() 
#cap.release()
cv2.destroyAllWindows()