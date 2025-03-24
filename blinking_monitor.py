import time
from datetime import date
import cv2
import numpy as np
import dlib
import imutils
import gspread
from imutils.video import VideoStream
from imutils import face_utils
from gpiozero import Buzzer
import drivers

# Initialize buzzer and LED (connected to GPIO pins)
buzzer = Buzzer(23)
led = Buzzer(24)

# Connect to Google Sheets
sa = gspread.service_account(filename="keys.json")
sh = sa.open("blink outputs")
wks = sh.worksheet("Sheet1")

# Read threshold values from Google Sheets
th = int(wks.cell(1, 2).value)  # Blink threshold
nin = int(wks.cell(2, 2).value)  # Number of records
er = float(wks.cell(3, 2).value)  # Eye aspect ratio threshold
T = int(wks.cell(4, 2).value)  # Monitoring time duration
rec = nin + 6  # Record position in the spreadsheet

# Initialize LCD display
display = drivers.Lcd()
display.lcd_display_string("Welcome", 1)
time.sleep(2)

# Start video stream
cap = VideoStream(src=0).start()

# Load face detector and facial landmark predictor
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Function to compute Euclidean distance between two points
def compute(ptA, ptB):
    return np.linalg.norm(ptA - ptB)

# Function to determine if a blink has occurred
def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)  # Distance between upper and lower eyelids
    down = compute(a, f)  # Distance between the two corners of the eye
    ratio = up / (2.0 * down)
    return 0 if ratio < er else 1

while True:
    blinks = 0
    start = time.time()
    
    try:
        while time.time() - start < T:
            frame = cap.read()
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, 
                                              minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            
            for (x, y, w, h) in faces:
                face = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
                landmarks = predictor(gray, face)
                landmarks = face_utils.shape_to_np(landmarks)
                
                # Detect blinks for left and right eyes
                left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
                right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])
                
                if left_blink == 0 or right_blink == 0:
                    blinks += 1
                    display.lcd_clear()
                    display.lcd_display_string(f"Blinks: {blinks}", 1)
                    time.sleep(0.6)
                
            key = cv2.waitKey(1)
    except Exception:
        blinks = 100  # If an error occurs, set blinks to 100 (face not found)
    
    # Get current date
    d4 = date.today().strftime("%b-%d-%Y")
    
    # Handle blink scenarios
    if blinks < th:
        display.lcd_clear()
        display.lcd_display_string(f"Blinks: {blinks}", 1)
        display.lcd_display_string("Blink more please", 2)
        
        # Update Google Sheet
        wks.update_cell(rec, 2, blinks)
        wks.update_cell(rec, 1, d4)
        nin += 1
        wks.update_cell(2, 2, nin)
        rec += 1
        
        # Trigger buzzer and LED
        for _ in range(2):
            buzzer.on()
            led.on()
            time.sleep(0.5)
            buzzer.off()
            led.off()
            time.sleep(0.5)
    
    elif blinks == 100:
        display.lcd_clear()
        display.lcd_display_string("Face not found", 1)
        time.sleep(1)
        nin = int(wks.cell(2, 2).value)
        rec = nin + 6
    
    else:
        display.lcd_clear()
        display.lcd_display_string(f"Blinks: {blinks}", 1)
        display.lcd_display_string("Normal rate", 2)
        time.sleep(0.5)
        
        # Update Google Sheet
        wks.update_cell(rec, 2, blinks)
        wks.update_cell(rec, 1, d4)
        nin += 1
        wks.update_cell(2, 2, nin)
        rec += 1
    
    # Cleanup
    cv2.destroyAllWindows()
    cap.stop()
