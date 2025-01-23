import requests
import pandas as pd
import sys
import os
from logs import write_normal_log, write_error_log

API_URL = "https://api.tarkov.dev/graphql"

def get_xlsx_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, 'ammo_offsets.xlsx')

def run_query(query):
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(API_URL, headers=headers, json={'query': query})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"GraphQL query failed with status {response.status_code}")
    except Exception as e:
        print(f"Error during API request: {e}")
        raise

def get_ammo_offsets(ammo_name):
    try:
        # Read the Excel file and load it into a DataFrame
        df = pd.read_excel(get_xlsx_path())  # Load Excel file
        
        # Trim any leading/trailing whitespace from the ammo name in both the input and DataFrame
        ammo_name = ammo_name.strip()
        
        # Ensure 'shortName' is also stripped of whitespace in the DataFrame
        df['shortName'] = df['shortName'].str.strip()
        
        # Log the ammo name and the first few rows of the DataFrame for debugging
        write_normal_log(f"Searching for ammo: '{ammo_name}'")
        write_normal_log(f"Excel Data: {df.head()}")  # Print out the first few rows of the data for debugging
        
        # Perform a case-insensitive match for the ammo name
        matched_rows = df[df['shortName'].str.lower() == ammo_name.lower()]
        
        # Log the matched rows for debugging
        write_normal_log(f"Found rows: {matched_rows}")
        
        # If any matches are found, return the offsets
        if not matched_rows.empty:
            return matched_rows['offset'].tolist()  # Return a list of offsets
        else:
            write_error_log(f"Ammo type '{ammo_name}' not found in the database.")
            return []
    
    except Exception as e:
        write_error_log(f"Error reading Excel file: {e}")
        print(f"Error reading Excel file: {e}")
        return []