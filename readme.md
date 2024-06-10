# License Plate Recognition System

This project is a license plate recognition system that uses RTSP camera feeds to detect and recognize vehicle license plates. The recognized license plates, along with their passage times and camera codes, are logged for further analysis.

## Features

- Capture and process RTSP camera feeds to detect license plates.
- Save detected license plate regions as images.
- Recognize license plates using the Plate Recognizer API.
- Log recognized license plates, passage times, and camera codes.
- Clean up old log files periodically to manage storage.

## Project Structure

- `preprocess.py`: Captures RTSP camera feeds, detects license plates, and saves the plate regions.
- `recognize.py`: Recognizes the saved license plate regions and logs the results.
- `post-process.py`: Processes the JSON response from the Plate Recognizer API.
- `cleaner.py`: Cleans up old log files that are older than a specified duration.
- `cameras.json`: Stores RTSP camera links and corresponding camera codes (needs to be created manually).
- `token.txt`: Stores the Plate Recognizer API token (needs to be created manually).

## Setup

### Requirements

- Python 3.x
- Required Python packages:
  - `requests`
  - `opencv-python`
  - `pillow`

Install the required packages using pip:
```sh
pip install requests opencv-python pillow
```

### Files to Create

1. **`cameras.json`**: This file stores RTSP camera links and corresponding camera codes. Create this file manually with the following structure:

```json
{
    "cameras": [
        {
            "camera_code": "IN1",
            "rtsp_link": "rtsp://username:password@ip_address:port/stream1"
        },
        {
            "camera_code": "IN2",
            "rtsp_link": "rtsp://username:password@ip_address:port/stream2"
        },
        {
            "camera_code": "OUT1",
            "rtsp_link": "rtsp://username:password@ip_address:port/stream3"
        },
        {
            "camera_code": "OUT2",
            "rtsp_link": "rtsp://username:password@ip_address:port/stream4"
        }
    ]
}
```

2. **`token.txt`**: This file stores the Plate Recognizer API token. Create this file manually and add your API token in the following format:
```txt
YOUR_API_TOKEN_HERE
```

## Running the Project

1. **Start the Preprocess Script**:
   This script captures RTSP camera feeds, detects license plates, and saves the plate regions.
   ```sh
   python3 preprocess.py
   ```

2. **Recognition Script**:
   This script is automatically triggered by the preprocess script whenever a plate is detected. It recognizes the saved license plate regions and logs the results.

3. **Cleaner Script**:
   The cleaner script is also automatically triggered by the recognition script to clean up old log files.

## Logging

- The recognized license plates, along with their passage times and camera codes, are logged in `pass_log.json`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
