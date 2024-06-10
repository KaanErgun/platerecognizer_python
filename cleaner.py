import os
import time
from datetime import datetime, timedelta

# Directory to clean
log_dir = "log"

# Time threshold in seconds (currently set to 60 seconds for testing)
time_threshold_seconds = 60

# Calculate the time threshold
time_threshold = datetime.now() - timedelta(seconds=time_threshold_seconds)

# Iterate through files in log directory
for filename in os.listdir(log_dir):
    file_path = os.path.join(log_dir, filename)
    file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))

    if file_modified_time < time_threshold:
        os.remove(file_path)
        print(f"Removed {file_path}")

print("Cleaner finished.")
