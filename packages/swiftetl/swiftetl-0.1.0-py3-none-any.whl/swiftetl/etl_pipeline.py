# swiftetl/swiftetl/etl_pipeline.py

import sqlite3
import pandas as pd

class ETLPipeline:
    def __init__(self, source, database):
        self.source = source
        self.database = database
        self.data = None

    def extract_data(self):
        """Extract data from the source."""
        # For CSV files
        if self.source.endswith('.csv'):
            self.data = pd.read_csv(self.source)
            print(f"Data extracted from {self.source}.")
        else:
            raise ValueError("Unsupported source format.")

    def transform_data(self):
        """Transform the data as needed."""
        # Example transformation: Drop rows with missing values
        self.data.dropna(inplace=True)
        print("Data transformed (missing values dropped).")

    def load_data(self):
        """Load data into the SQLite database."""
        conn = sqlite3.connect(self.database)
        self.data.to_sql('data_table', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Data loaded into {self.database}.")

