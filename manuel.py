import sys
import requests
from pprint import pprint

# Platerecognizer API key
API_KEY = '0d0199716980f3f8aef99eeb08e2b345c493e72f'

def recognize_plate(image_path):
    regions = ["au"]  # Change to your country or desired regions
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),  # Optional
            files=dict(upload=image_file),
            headers={'Authorization': f'Token {API_KEY}'}
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
