import sys
import requests
from pprint import pprint

def get_api_key():
    with open('token.txt', 'r') as file:
        return file.read().strip()

def recognize_plate(image_path):
    api_key = get_api_key()
    regions = ["au"]  # Change to your country or desired regions
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=image_file),
            headers={'Authorization': f'Token {api_key}'}
        )

        if response.status_code == 200:
            data = response.json()
            pprint(data)
            return data
        else:
            print(f"Error: {response.status_code}")
            pprint(response.json())
            return None

# Get the image path from command line arguments
if len(sys.argv) != 2:
    print("Usage: python3 recognize.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]
result = recognize_plate(image_path)

if result and result['results']:
    print("License Plate Recognition Result:")
    for res in result['results']:
        print(f"Plate: {res['plate']}")
        print(f"Confidence: {res['score']}")
        print(f"Vehicle Type: {res['vehicle']['type']}")
        print("----")
else:
    print("Failed to recognize the plate.")
