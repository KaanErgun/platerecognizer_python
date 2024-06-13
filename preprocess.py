import cv2
import threading
import time
import os
from datetime import datetime
import json

stop_event = threading.Event()

# Function to capture, crop, resize, and save image from camera
def capture_and_save(camera_code, rtsp_link, roi, use_roi):
    try:
        cap = cv2.VideoCapture(rtsp_link)
        if not cap.isOpened():
            print(f"Camera {camera_code} could not be opened.")
            return

        while not stop_event.is_set():
            ret, frame = cap.read()
            if ret:
                # Convert to 1:1 aspect ratio by cropping sides if needed
                h, w, _ = frame.shape
                if w > h:
                    diff = (w - h) // 2
                    square_frame = frame[:, diff:diff+h]
                elif h > w:
                    diff = (h - w) // 2
                    square_frame = frame[diff:diff+w, :]
                else:
                    square_frame = frame

                # Resize to 500x500
                resized_frame = cv2.resize(square_frame, (500, 500))

                if use_roi:
                    roi_x, roi_y, roi_w, roi_h = roi
                    # Apply ROI
                    roi_frame = resized_frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]
                else:
                    roi_frame = resized_frame

                # Debug: Save the cropped and resized image for verification
                debug_filename = f"log/{camera_code}_debug.jpg"
                cv2.imwrite(debug_filename, roi_frame)

                gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
                plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
                plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                if len(plates) > 0:
                    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                    filename = f"log/{camera_code}_{timestamp}.jpg"
                    cv2.imwrite(filename, roi_frame)
                    # Trigger recognize.py with the saved image filename
                    os.system(f"python recognize.py {filename} {camera_code}")
                    time.sleep(2)  # Adjust sleep time to control the request frequency
                else:
                    print(f"No plate detected from camera {camera_code}")
            else:
                print(f"Failed to capture frame from camera {camera_code}")
            time.sleep(10)  # Capture every 10 seconds, adjust as needed

        cap.release()
    except Exception as e:
        print(f"Error with camera {camera_code}: {e}")

def cleaner_trigger():
    while not stop_event.is_set():
        os.system("python cleaner.py")
        time.sleep(60)  # Run cleaner.py every 60 seconds for testing

def main():
    # Read cameras.json
    with open('cameras.json') as f:
        cameras = json.load(f)

    # Read ROI.json
    with open('ROI.json') as f:
        rois = json.load(f)

    # Set use_roi switch
    use_roi = True  # Change to False to disable ROI processing

    # Create a thread for each camera
    threads = []
    for camera in cameras:
        camera_code = camera['code']
        rtsp_link = camera['rtsp']
        if camera_code in rois:
            roi = (rois[camera_code]['x'], rois[camera_code]['y'], rois[camera_code]['w'], rois[camera_code]['h'])
            thread = threading.Thread(target=capture_and_save, args=(camera_code, rtsp_link, roi, use_roi))
            threads.append(thread)
            thread.start()
        else:
            print(f"No ROI found for camera {camera_code}")

    # Start cleaner trigger thread
    cleaner_thread = threading.Thread(target=cleaner_trigger)
    cleaner_thread.start()

    # Wait for 'q' key to stop all threads
    print("Press 'q' to quit.")
    while True:
        if input().strip().lower() == 'q':
            stop_event.set()
            break

    # Join threads to main thread
    for thread in threads:
        thread.join()

    # Join cleaner thread
    cleaner_thread.join()

    print("Application terminated.")

if __name__ == "__main__":
    main()
