import os
import pandas as pd
import requests
import csv

class InputHandler:
    def __init__(self):
        self.data = None
        

    def load_data_from_csv(self, file_path):
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
            self.data = pd.read_csv(file_path, sep=inferred_sep)
            print(f"Data loaded successfully from {file_path}")
            print(f'Data shape: {self.data.shape}')
            return self.data
        except Exception as e:
            raise ValueError(f"Error reading the CSV file with inferred delimiter: {e}")



    def load_data_from_txt(self, file_path):
        """Loads data from a TXT file."""
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                self.data = file.readlines()
            print(f"Data loaded successfully from {file_path}")
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    def load_data_from_parquet(self, file_path):
        """Loads data from a Parquet file."""
        if os.path.exists(file_path):
            self.data = pd.read_parquet(file_path)
            print(f"Data loaded successfully from {file_path}")            
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    def load_data_from_url(self, url):
        """Loads data from a URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            self.data = pd.read_csv(pd.compat.StringIO(response.text))  # Assuming CSV data
            print(f"Data loaded successfully from {url}")
        except Exception as e:
            raise ValueError(f"Error loading data from URL: {e}")
        


# # Example usage:
# # csv_data = load_data_from_csv('path_to_your_file.csv')
# # txt_data = load_data_from_txt('path_to_your_file.txt')
# # parquet_data = load_data_from_parquet('path_to_your_file.parquet')
# # url_data = load_data_from_url('http://example.com/data.csv')
