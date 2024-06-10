import sys
import json
from datetime import datetime
import threading
import os

log_lock = threading.Lock()

def process_result(json_filename, camera_code):
    with open(json_filename, 'r') as file:
        data = json.load(file)

    for result in data['results']:
        if result['score'] >= 0.85:
            plate = result['plate']
            print(f"Plate: {plate}, Score: {result['score']}, Camera: {camera_code}")
            log_passing_vehicle(plate, camera_code)

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
        print("Usage: python post-process.py <json_filename> <camera_code>")
        sys.exit(1)
    
    json_filename = sys.argv[1]
    camera_code = sys.argv[2]
    process_result(json_filename, camera_code)
