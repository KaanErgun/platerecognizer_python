import requests
import sys
import json
import os
from datetime import datetime

def recognize_plate(image_path, camera_code):
    with open('token.txt', 'r') as file:
        token = file.read().strip()

    with open(image_path, 'rb') as img:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            files=dict(upload=img),
            headers={'Authorization': f'Token {token}'}
        )
    
    result = response.json()
    
    # Save JSON result
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    json_filename = f"log/{camera_code}_{timestamp}.json"
    with open(json_filename, 'w') as json_file:
        json.dump(result, json_file)
    
    # Trigger post-process.py
    os.system(f"python post-process.py {json_filename} {camera_code}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python recognize.py <image_path> <camera_code>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    camera_code = sys.argv[2]
    recognize_plate(image_path, camera_code)
