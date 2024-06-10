import cv2
import json
import os

def select_roi(frame):
    roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select ROI")
    return roi

def save_roi_to_json(camera_code, roi, file_path="ROI.json"):
    roi_data = {}
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            roi_data = json.load(f)
    
    roi_data[camera_code] = {
        "x": int(roi[0]),
        "y": int(roi[1]),
        "w": int(roi[2]),
        "h": int(roi[3])
    }

    with open(file_path, 'w') as f:
        json.dump(roi_data, f, indent=4)
    print(f"ROI for camera {camera_code} saved to {file_path}")

def main():
    # Read cameras.json
    with open('cameras.json') as f:
        cameras = json.load(f)

    for camera in cameras:
        camera_code = camera['code']
        rtsp_link = camera['rtsp']
        cap = cv2.VideoCapture(rtsp_link)
        if not cap.isOpened():
            print(f"Camera {camera_code} could not be opened.")
            continue

        ret, frame = cap.read()
        if not ret:
            print(f"Failed to capture frame from camera {camera_code}")
            continue

        # Convert to 1:1 aspect ratio by cropping sides if needed
        h, w, _ = frame.shape
        if w > h:
            diff = (w - h) // 2
            frame = frame[:, diff:w-diff]
        elif h > w:
            diff = (h - w) // 2
            frame = frame[diff:h-diff, :]

        frame = cv2.resize(frame, (500, 500))

        while True:
            cv2.imshow(f"Camera {camera_code}", frame)
            key = cv2.waitKey(0) & 0xFF

            if key == ord('n'):  # Move to next camera
                break
            elif key == ord('e'):  # Enter edit mode
                roi = select_roi(frame)
                save_roi_to_json(camera_code, roi)
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
