import cv2
import datetime
import subprocess
import time
import os

def save_plate_region(camera_code):
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 5)  # Set FPS to 5

    log_dir = 'log'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to capture image")
            break
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Load the pre-trained Haar Cascade classifier for license plate detection
        plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
        
        # Detect license plates in the frame
        plates = plate_cascade.detectMultiScale(gray, 1.1, 10)
        
        # If a plate is detected, save the region and trigger recognize.py
        for (x, y, w, h) in plates:
            plate_region = frame[y:y+h, x:x+w]
            current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
            file_name = os.path.join(log_dir, f"{camera_code}_{current_time}.jpg")
            cv2.imwrite(file_name, plate_region)
            print(f"Saved plate region as {file_name}")
            
            # Trigger recognize.py with the saved image file name
            subprocess.run(["python3", "recognize.py", file_name])
            time.sleep(20)  # Add a delay of 20 seconds
        
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

# Example usage
camera_code = 'camera1'
save_plate_region(camera_code)
