import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sdv.metadata import SingleTableMetadata

from sdv.metadata import Metadata


class DataPreprocessor:
    def __init__(self, data=None):
        self.data = data
        self.metadata = {}

    def check_real_data_availability(self):
        """Check if real data (DataFrame) is available and not empty."""
        if self.data is not None and not self.data.empty:
            # print("Real data is available.")
            return True
        else:
            print("No real data available or the data is empty.")
            return False

    def handle_missing_values(self, strategy='mean'):
        """Handle missing values in the data using a specified strategy."""
        if self.check_real_data_availability():
            for column in self.data.columns:
                if self.data[column].isnull().any():  # Only handle if there are missing values
                    if self.data[column].dtype in [int, float]:  # Numeric columns
                        if strategy == 'mean':
                            self.data[column].fillna(self.data[column].mean(), inplace=True)
                        elif strategy == 'median':
                            self.data[column].fillna(self.data[column].median(), inplace=True)
                        elif strategy == 'mode':
                            self.data[column].fillna(self.data[column].mode()[0], inplace=True)
                        elif strategy == 'drop':
                            self.data.dropna(subset=[column], inplace=True)
                        else:
                            raise ValueError("Invalid strategy for handling missing values.")
                    else:
                        # Handle non-numeric columns by filling with mode or dropping
                        if strategy == 'mode':
                            self.data[column].fillna(self.data[column].mode()[0], inplace=True)
                        elif strategy == 'drop':
                            self.data.dropna(subset=[column], inplace=True)
                        # You may want to add other strategies here if needed

    def encode_categorical_data(self):
        """Encode categorical variables using LabelEncoder."""
        if self.check_real_data_availability():
            for column in self.data.select_dtypes(include=['object']).columns:
                le = LabelEncoder()
                self.data[column] = le.fit_transform(self.data[column].astype(str))  # Convert to string before encoding
        else:
            raise ValueError("No real data to preprocess.")

    def scale_numerical_data(self):
        """Scale numerical data using StandardScaler."""
        if self.check_real_data_availability():
            scaler = StandardScaler()
            numeric_cols = self.data.select_dtypes(include=['float64', 'int64']).columns
            self.data[numeric_cols] = scaler.fit_transform(self.data[numeric_cols])
        else:
            raise ValueError("No real data to preprocess.")

    def convert_timestamps(self):
        """Convert any timestamp columns to a standard datetime format."""
        if self.check_real_data_availability():
            for column in self.data.columns:
                if pd.api.types.is_datetime64_any_dtype(self.data[column]):
                    # Convert to a standard datetime format if not already
                    self.data[column] = pd.to_datetime(self.data[column], errors='coerce')
                    print(f"Converted column '{column}' to datetime.")
        else:
            raise ValueError("No real data to preprocess.")

    def extract_metadata(self):
        """Extract metadata from the data using SDV."""
        if self.check_real_data_availability():
            print("Extracting metadata using SDV...")
            metadata = Metadata.detect_from_dataframe(self.data)

            metadata.detect_from_dataframe(self.data)
            self.metadata =  metadata# metadata.to_dict()  # Convert metadata to dictionary format
            print("Metadata extracted using SDV.")
            return self.metadata
        else:
            raise ValueError("No real data to extract metadata from.")

    def preprocess_data(self, handle_missing='mean'):
        """Perform preprocessing including handling missing values, encoding, scaling, converting timestamps, and metadata extraction."""
        if self.check_real_data_availability():
            print(f"Preprocessing data. Data shape: {self.data.shape}")

            # Handle missing values
            self.handle_missing_values(strategy=handle_missing)

            # # Convert timestamp columns
            # self.convert_timestamps()

            # # Encode categorical data
            # self.encode_categorical_data()

            # # Scale numerical data
            # self.scale_numerical_data()

            # Extract metadata using SDV
            metadata = self.extract_metadata()

            print("Preprocessing complete.")
            return self.data, metadata  # Return processed data and metadata
        else:
            raise ValueError("No real data to preprocess.")

# Example usage:
# df = pd.read_csv('your_data.csv')
# preprocessor = DataPreprocessor(data=df)
# processed_data, metadata = preprocessor.preprocess_data()
