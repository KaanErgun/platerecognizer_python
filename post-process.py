import sys
import json

def process_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    if 'results' in data:
        for result in data['results']:
            if result['score'] >= 0.85:
                print("License Plate Detected:")
                print(f"Plate: {result['plate']}")
                ##print(f"Confidence: {result['score']}")
                ##print(f"Vehicle Type: {result['vehicle']['type']}")
                print("----")
            else:
                print("No plates with sufficient confidence found.")
    else:
        print("No results found in the JSON file.")

# Get the JSON file path from command line arguments
if len(sys.argv) != 2:
    print("Usage: python3 post-process.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
process_json(json_file_path)
