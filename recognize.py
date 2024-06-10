import sys
import requests
import json
import subprocess
import os

# Platerecognizer API key
API_KEY = '0d0199716980f3f8aef99eeb08e2b345c493e72f'

def recognize_plate(image_path):
    regions = ["au"]  # Change to your country or desired regions
    log_dir = 'log'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    with open(image_path, 'rb') as image_file:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=image_file),
            headers={'Authorization': f'Token {API_KEY}'}
        )

        data = response.json()
        # Save JSON response to a file regardless of the status code
        json_file = image_path.replace('.jpg', '.json')
        with open(json_file, 'w') as outfile:
            json.dump(data, outfile)
        if os.path.exists(json_file):
            print(f"JSON response saved to {json_file}")
            return json_file
        else:
            print("Failed to save the JSON file.")
            return None

# Get the image path from command line arguments
if len(sys.argv) != 2:
    print("Usage: python3 recognize.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]
json_file = recognize_plate(image_path)

if json_file:
    # Trigger post-processing
    subprocess.run(["python3", "post-process.py", json_file])
    
    # Debug information to check if cleaner.py is being triggered
    print("Triggering cleaner.py to clean up old files in the log directory...")
    result = subprocess.run(["python3", "cleaner.py"])
    if result.returncode == 0:
        print("cleaner.py executed successfully.")
    else:
        print("Failed to execute cleaner.py.")
else:
    print("Failed to recognize the plate.")
