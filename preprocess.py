import cv2
import threading
import time
import os
from datetime import datetime
import json

# Function to capture and save image from camera
def capture_and_save(camera_code, rtsp_link):
    try:
        cap = cv2.VideoCapture(rtsp_link)
        if not cap.isOpened():
            print(f"Camera {camera_code} could not be opened.")
            return

        # Load pre-trained Haar Cascade classifier for license plate detection
        plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

        while True:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(plates) > 0:
                    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                    filename = f"log/{camera_code}_{timestamp}.jpg"
                    cv2.imwrite(filename, frame)
                    # Trigger recognize.py with the saved image filename
                    os.system(f"python recognize.py {filename} {camera_code}")
                    time.sleep(2)  # Adjust sleep time to control the request frequency
                else:
                    print(f"No plate detected from camera {camera_code}")
            else:
                print(f"Failed to capture frame from camera {camera_code}")
            time.sleep(10)  # Capture every 10 seconds, adjust as needed
    except Exception as e:
        print(f"Error with camera {camera_code}: {e}")

def cleaner_trigger():
    while True:
        os.system("python cleaner.py")
        time.sleep(60)  # Run cleaner.py every 60 seconds for testing

def main():
    # Read cameras.json
    with open('cameras.json') as f:
        cameras = json.load(f)

    # Create a thread for each camera
    threads = []
    for camera in cameras:
        camera_code = camera['code']
        rtsp_link = camera['rtsp']
        thread = threading.Thread(target=capture_and_save, args=(camera_code, rtsp_link))
        threads.append(thread)
        thread.start()

    # Start cleaner trigger thread
    cleaner_thread = threading.Thread(target=cleaner_trigger)
    cleaner_thread.start()

    # Join threads to main thread
    for thread in threads:
        thread.join()

    # Join cleaner thread
    cleaner_thread.join()

if __name__ == "__main__":
    main()
