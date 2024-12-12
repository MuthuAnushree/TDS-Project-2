# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#   "pandas",
#   "requests",
#   "seaborn",
#   "matplotlib",
#   "tabulate"
# ]
# ///

import os
import sys
import pandas as pd
import numpy as np
import requests
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns
import tabulate
from datetime import datetime

api_key = os.getenv("API_KEY")

'''if api_key:
    print(f"API Key: {api_key}")
else:
    print("API Key not found!")'''


#---------Loading CSV
def load_csv(filename):
    try:
        data = pd.read_csv(filename)
        print(f"Data loaded successfully! Shape: {data.shape}")
        return data
    
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{filename}' is empty or invalid.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Check if a filename is provided
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <filename>")
        sys.exit(1)
    
    # Get the filename
    csv_filename = sys.argv[1]
    
    # Analyze the dataset
    data=load_csv(csv_filename)

# Prompt the user for a file path (or use a GUI file picker in an enhanced version)
#file_path = "D:\ANU Books\DATA SCIENCE AND PROGRAMMING\TDS\Project2\goodreads.csv"
#input("Enter the path to your CSV file: ")
#data = load_csv(file_path)

# Display initial rows
if data is not None:
    print("First few rows of the data:")
    print(data.head())

#---------Cleaning Data---------
def clean_data(data):
    try:
        print("\n--- Cleaning Data ---")
        
        # Check for missing values
        missing_counts = data.isnull().sum()
        print("\nMissing Values per Column:")
        print(missing_counts)
        
        # Optionally handle missing values
        data = data.fillna(method='ffill').fillna(method='bfill')  # Forward and backward fill
        
        # Remove duplicates
        initial_shape = data.shape
        data = data.drop_duplicates()
        print(f"\nRemoved {initial_shape[0] - data.shape[0]} duplicate rows.")
        
        # Standardize column names
        data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]
        print("\nStandardized Column Names:")
        print(data.columns.tolist())
        
        # Check for columns that may be convertible to numeric
        for col in data.columns:
            if data[col].dtype == object: 
        # Check if the column contains numeric-like data
                if data[col].str.isnumeric().all():
                    try:
                        data[col] = pd.to_numeric(data[col])
                        print(f"Converted column '{col}' to numeric.")
                    except Exception as e:
                        print(f"Error converting column '{col}' to numeric: {e}")
                else:
                    print(f"Skipped column '{col}' as it contains non-numeric values.")


        print("\nData cleaned successfully!")
        return data

    except Exception as e:
        print(f"An error occurred during data cleaning: {e}")
        return data

# Clean the loaded data
cleaned_data = clean_data(data)

# Display basic info about cleaned data
if cleaned_data is not None:
    print("\n--- Cleaned Data Info ---")
    print(cleaned_data.info())
    print("\nSample of Cleaned Data:")
    print(cleaned_data.head())

# Meta data summary
def generic_analysis(data):
    print("\n--- Generic Analysis ---")
    # Summary statistics
    summary_stats = data.describe(include='all')  # Includes object columns
    print("\nSummary Statistics:")
    print(summary_stats)

    # Missing values
    missing_values = data.isnull().sum()
    #print("\nMissing Values:")
    #print(missing_values)

    # Correlation matrix (for numeric columns)
    numeric_columns = data.select_dtypes(include=["number"])
    correlation_matrix = numeric_columns.corr()
    #print("\nCorrelation Matrix:")
    

    # Frequency distribution for string/categorical columns
    categorical_columns = data.select_dtypes(include=["object", "category"])
    categorical_distributions = {}
    for col in categorical_columns:
        categorical_distributions[col] = data[col].value_counts().to_dict()

    '''print("\nCategorical Distributions:")
    for col, dist in categorical_distributions.items():
        print(f"{col}:\n{dist}")'''

    # Prepare metadata for LLM
    metadata = {
        "example_rows": data.head(3).to_dict(orient='records'),
        "columns": [{"name": col, "type": str(data[col].dtype)} for col in data.columns],
        "summary_statistics": summary_stats.to_dict(),
        "missing_values": missing_values.to_dict(),        
        "categorical_distributions": categorical_distributions,
        "correlation_matrix":correlation_matrix
    }

    return metadata

def llm_sample_data(data, max_length=312):
    """
    Generates a sample string from the dataset, ensuring it fits within the max length.
    """
    # Take the first row for simplicity
    limited_rows = data.head(1).to_dict(orient="records")  # Only first row
    sample_as_string = json.dumps(limited_rows)  # Convert to string
    
    # Truncate if it exceeds max_length
    '''if len(sample_as_string) > max_length:
        sample_as_string = sample_as_string[:max_length - 3] + "..."  # Truncate with ellipsis'''

    return {"example_rows": sample_as_string}


def query_llm_via_proxy(sample, task="analyze"):

    example_rows_as_string = json.dumps(sample["example_rows"])  
    prompt=(
        "I need a Python script that can perform the following analysis on any given dataset (CSV format):"+
    "\nUse error handling while applying the basic analysis."+
    "\n1. Identify quantitative numerical data columns and perform basic descriptive statistics on the appropriate numerical columns (e.g., mean, median, standard deviation)."+
    "\n2. Only for numerical data that are quantitative and not identity numbers, calculate correlations between features and identify potential relationships."+
    "\n3. If there is a time-related column (like dates), aggregate the data by time (e.g., monthly or yearly) and plot the trend."+
    "\n4. Generate suitable visualizations depending on the data: histograms for distributions, line charts for time series, and bar charts for category comparisons."+
    "\n5. Use pandas for data manipulation, and matplotlib or seaborn for plotting. Save any plots as PNG images and save the summary in a README.md file."+
    
    f"\n7. Here is a sample of the dataset: {example_rows_as_string}"+
    
    "\nGive only the Python script, with uncommented function call(s) in response. The script should accept the filename as a command-line argument"+
    "and handle errors if the file does not exist or is invalid."
    )

    payload = {
        #"prompt":prompt,
        "model": "gpt-4o-mini", 
        "messages": [{"role": "system", "content": prompt}],
        #"task": task,
        #"metadata": metadata
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"  # Assuming JSON payload
    }

    
    def send_request(prompt):
        try:
            response = requests.post("https://aiproxy.sanand.workers.dev/openai/v1/chat/completions", json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error from AI proxy: {response.status_code}, {response.text}")
                return None
        except Exception as e:
            print(f"Error during POST request: {e}")
            return None

    def fix_code_with_error(error_message, generated_code):
        # Modify the prompt to include the error and ask for corrections
        new_prompt = f"{generated_code}\n\nError: {error_message}\n\nPlease fix the code above and return only the corrected code."
        return new_prompt

    # Generate initial code from LLM
    response_json = send_request(prompt)
    if response_json:
        generated_code = response_json['choices'][0]['message']['content']
        print("Generated code:", generated_code)
    else:
        return "Error generating code from LLM."

    # Try to execute and catch any errors
    while True:
        try:
            exec(generated_code)  # Execute the generated code
            print("Code executed successfully without errors.")
            break  # Exit the loop if no errors occur
        except Exception as e:
            error_message = str(e)
            print(f"Error encountered: {error_message}")
            # Fix the code by sending the error to the LLM and asking for corrections
            prompt_for_fix = fix_code_with_error(error_message, generated_code)
            response_json = send_request(prompt_for_fix)
            if response_json:
                generated_code = response_json['choices'][0]['message']['content']
                print(f"Corrected code: {generated_code}")
            else:
                return "Error re-trying code generation."
    return generated_code

def extract_code(response_content):
    """
    Extracts the code block from LLM response content.

    Args:
        response_content (str): The full text response from the LLM.
    
    Returns:
        str: Extracted code or the original content if no code blocks are found.
    """
    # Use regex to find text enclosed in triple backticks
    match = re.search(r"```(?:python)?\n(.*?)```", response_content, re.DOTALL)
    if match:
        return match.group(1).strip()  # Extract and strip any leading/trailing whitespace
    return response_content  # If no code block is found, return the original content


# Step 3: Safely Execute the Code
def execute_code(generated_code, globals_=None, locals_=None):
    try:
        exec(generated_code, globals_, locals_)
    except Exception as e:
        print(f"Error executing code: {e}")


# Main Workflow
if cleaned_data is not None:
    # Step 1: Analyze Data
    metadata = generic_analysis(cleaned_data)
    sample=llm_sample_data(cleaned_data)
    #sample=list(sample)
    #print(metadata)
    # Step 2: Query LLM via Proxy
    llm_response=query_llm_via_proxy(sample)
    code_from_llm = extract_code(llm_response)
    
    # Step 3: Execute Code Safely
    print(code_from_llm)
    execute_code(code_from_llm)

'''metadata = generic_analysis(cleaned_data)
sample=llm_sample_data(cleaned_data)
print(sample)'''
#print(sample)
