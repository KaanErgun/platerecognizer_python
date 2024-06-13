import sys
import json
from datetime import datetime
import threading
import os
from difflib import SequenceMatcher

log_lock = threading.Lock()

def load_registered_plates():
    plates_file = 'plates.json'
    if os.path.exists(plates_file):
        with open(plates_file, 'r') as file:
            return json.load(file)
    return []

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def is_authorized_plate(plate):
    registered_plates = load_registered_plates()
    for registered_plate in registered_plates:
        if similar(plate, registered_plate['plate']) >= 0.8:
            return True
    return False

def process_result(json_filename, camera_code):
    with open(json_filename, 'r') as file:
        data = json.load(file)

    for result in data['results']:
        if result['score'] >= 0.85:
            plate = result['plate']
            print(f"Plate: {plate}, Score: {result['score']}, Camera: {camera_code}")
            log_passing_vehicle(plate, camera_code)

            if is_authorized_plate(plate):
                print("Authorized")
            else:
                print("Unauthorized")

def log_passing_vehicle(plate, camera_code):
    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "plate": plate,
        "camera_code": camera_code
    }

    log_file = 'pass_log.json'

    with log_lock:
        if os.path.exists(log_file):
            with open(log_file, 'r+') as file:
                data = json.load(file)
                data.append(log_data)
                file.seek(0)
                json.dump(data, file, indent=4)
        else:
            with open(log_file, 'w') as file:
                json.dump([log_data], file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 post-process.py <json_filename> <camera_code>")
        sys.exit(1)
    
    json_filename = sys.argv[1]
    camera_code = sys.argv[2]
    process_result(json_filename, camera_code)
