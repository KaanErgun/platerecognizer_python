import os
import time

def clean_log_directory(log_dir, max_age_minutes=1):
    # Get the current time
    now = time.time()
    
    # Convert max age to seconds
    max_age_seconds = max_age_minutes * 60

    print(f"Cleaning log directory: {log_dir}")
    # Iterate over all files in the log directory
    for filename in os.listdir(log_dir):
        file_path = os.path.join(log_dir, filename)
        
        # Check if the file is older than max_age_seconds
        file_age = now - os.stat(file_path).st_mtime
        print(f"Checking file: {file_path}, age: {file_age} seconds")
        if file_age > max_age_seconds:
            print(f"Deleting file: {file_path}")
            os.remove(file_path)

# Define the log directory
log_dir = 'log'

# Ensure the log directory exists
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Clean the log directory
clean_log_directory(log_dir)
