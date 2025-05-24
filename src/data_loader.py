# data_loader.py for opening dataset files

import pandas as pd
import os
import zipfile

def load_dataset_from_zip(zip_path: str, filename: str, **kwargs) -> pd.DataFrame:
    """
    Loads a CSV or Excel file from within a ZIP archive into a DataFrame.
    
    Args:
        zip_path (str): Path to the ZIP file.
        filename (str): Name of the CSV or Excel file inside the ZIP.
        kwargs: Additional parameters passed to pd.read_csv or pd.read_excel.
    
    Returns:
        pd.DataFrame: Loaded DataFrame.
    
    Raises:
        FileNotFoundError: If the ZIP file does not exist.
        KeyError: If the specified file is not found in the ZIP.
        ValueError: If the file extension is not supported.
    """
    if not os.path.exists(zip_path):
        print(f"\n*** Error *** \nFile not found: {zip_path}")
        print("Current working directory:", os.getcwd())
        raise FileNotFoundError(f"File not found: {zip_path}")

    with zipfile.ZipFile(zip_path) as z:
        if filename not in z.namelist():
            raise KeyError(f"The file '{filename}' was not found in the ZIP archive.")
        
        with z.open(filename) as file:
            ext = os.path.splitext(filename)[1].lower()
            if ext == '.csv':
                df = pd.read_csv(file, **kwargs)
            elif ext in ['.xls', '.xlsx']:
                df = pd.read_excel(file, **kwargs)
            else:
                raise ValueError(f"Unsupported file extension '{ext}'. Only .csv, .xls and .xlsx are supported.")
    return df

def load_dataset_from_csv(path, **kwargs):
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"*** Error *** \nFile not found: {path}.")
        print("\nThis is your current", os.getcwd())
    
    df = pd.read_csv(path, **kwargs)
    
    return df

def load_dataset_from_excel(path, **kwargs):

    if not os.path.exists(path):
        raise FileNotFoundError(f"*** Error *** \nFile not found: {path}.")
        print("\nThis is your current", os.getcwd())

    df = pd.read_excel(path, **kwargs)
    
    return df

def load_dataset_from_list(list ):
    
    df = pd.DataFrame(list)
    
    return df 

def load_dataset_from_dict(dict ):
    
    df = pd.DataFrame.from_dict(dict, orient='columns')
    
    return df