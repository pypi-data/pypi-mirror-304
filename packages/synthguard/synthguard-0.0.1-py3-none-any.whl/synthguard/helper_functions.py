import os

def load_data(file_path):
    """Loads data from a given file path."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
        return data
    else:
        raise FileNotFoundError(f"File not found: {file_path}")
    
import os
import pandas as pd
import csv

def load_data_csv(file_path):
    """Loads data from a CSV file and infers the delimiter automatically."""
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check if the file has a .csv extension
    if not file_path.endswith('.csv'):
        raise ValueError(f"File is not a CSV: {file_path}")
    
    # Infer the delimiter using csv.Sniffer
    try:
        with open(file_path, 'r') as file:
            sample = file.read(1024)  # Read a sample of the file
            sniffer = csv.Sniffer()
            dialect = sniffer.sniff(sample)  # Infer the delimiter
            inferred_sep = dialect.delimiter
    except Exception as e:
        raise ValueError(f"Error inferring delimiter: {e}")
    
    # Load the data using the inferred delimiter
    try:
        data = pd.read_csv(file_path, sep=inferred_sep)
        return data
    except Exception as e:
        raise ValueError(f"Error reading the CSV file with inferred delimiter: {e}")


def save_to_file(content, file_path):
    """Saves given content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Data saved to {file_path}")


import datetime

def log_event(event_message, log_file="tool_log.txt"):
    """Logs events to a file with timestamps."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{timestamp} - {event_message}\n"
    
    with open(log_file, 'a') as file:
        file.write(log_message)
    
    print(f"Logged: {event_message}")


def validate_data_format(data, expected_format="csv"):
    """Validates that the data is in the expected format."""
    if not data.endswith(f".{expected_format}"):
        raise ValueError(f"Invalid data format. Expected {expected_format} format.")
    return True

def validate_not_empty(data):
    """Checks if the data is not empty."""
    if not data:
        raise ValueError("The data is empty.")
    return True


import json

def convert_dict_to_json(data_dict):
    """Converts a Python dictionary to a JSON string."""
    return json.dumps(data_dict, indent=4)

def convert_json_to_dict(json_string):
    """Converts a JSON string to a Python dictionary."""
    return json.loads(json_string)


import numpy as np

def calculate_mean(data):
    """Calculates the mean of a dataset."""
    return np.mean(data)

def calculate_standard_deviation(data):
    """Calculates the standard deviation of a dataset."""
    return np.std(data)


import time

def show_progress(current_step, total_steps):
    """Displays a simple progress indicator."""
    percentage = (current_step / total_steps) * 100
    print(f"Progress: {percentage:.2f}% ({current_step}/{total_steps})")
    time.sleep(0.5)


def handle_error(error_message, terminate=False):
    """Handles errors by logging and optionally terminating the process."""
    log_event(f"Error: {error_message}")
    print(f"Error: {error_message}")
    
    if terminate:
        exit(1)


import time

def start_timer():
    """Starts a timer to measure process duration."""
    return time.time()

def end_timer(start_time):
    """Ends the timer and returns the elapsed time."""
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
    return elapsed_time


from utils.helper_functions import log_event, handle_error, save_to_file

# Example of using the log function
log_event("Starting the synthetic data generation pipeline.")

try:
    # Code logic here...
    data = "This is a sample data."
    save_to_file(data, "output.txt")
except Exception as e:
    handle_error(f"An error occurred: {str(e)}", terminate=True)
