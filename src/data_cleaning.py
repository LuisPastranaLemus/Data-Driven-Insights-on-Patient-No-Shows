# data_cleaning.py for dataset cleaning

import numpy as np
import pandas as pd
import re
from tqdm import tqdm

def check_existing_missing_values(df, df_name="DataFrame"):
    
    missing_values = ['', ' ', 'N/A', 'none', 'None', 'null', 'NULL', 'NaN', 'nan', 'NAN', 'nat', 'NaT']
    
    print(f"> Dataframe: {df_name}\n")
    
    for column in df.columns:
        
        if df[column].dtype != 'object':
            
            continue
        
        else:
            
            if df[column].isin(missing_values).any():
                                
                print(f"*** Warning ***   > Mising values in '{column}': {df[column].isin(missing_values).sum()}")
            
            else:
                
                print(f"*** Warning ***   > No missing values in '{column}' found")
                
    print()

# Function used for assigning pd.NA to missing values
def replace_missing_values(df, include=None, exclude=None):
    
    missing_values = ['', ' ', 'N/A', 'none', 'None', 'null', 'NULL', 'NaN', 'nan', 'NAN', 'nat', 'NaT']
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
 
    for column in available_columns:
        
        if df[column].dtype != 'object':
            
            continue
        
        else:
            
            if df[column].isin(missing_values).any():
                
                df[column] = df[column].replace(missing_values, pd.NA)

    return df

# Function dataframe for format normalizing type 'object' (strings)
def normalize_df_string_format(df, include=None, exclude=None):
        
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
       if df[column].dtype != 'object':
           
           continue
       
       else:
                      
           df[column] = df[column].str.replace(r'[^\w\s]', ' ', regex=True)
           df[column] = df[column].str.replace(r'\s+', '_', regex=True)
           df[column] = df[column].str.replace(r'__+', '_', regex=True)
           df[column] = df[column].str.lower()
           df[column] = df[column].str.strip()
    
    return df

# Function for format normalizing type 'object' (strings)
def normalize_headers_string_format(df_header: list):
    
    header = []
    
    for title in df_header:
               
           title = re.sub(r'[^\w\s]', ' ', title)
           title = re.sub(r'\s+', '_', title)
           title = re.sub(r'__+', '_', title)
           title = title.lower()
           title = title.strip()
           
           header.append(title)
    
    return header

# Function for implicit duplicates
def detect_implicit_duplicates(df, include=None, exclude=None):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if column in exclude:
            
            continue  
        
        if df[column].dtype != 'object':
            
            continue
        
        # 1. Keep values that are single word with no separators with special chars
        column_values = df[column]
        column_values = column_values[column_values != '']
        column_values = column_values[column_values.apply(lambda x: len(re.split(r"[ \-\_']", x)) == 1)]

        # 2. Get base unique values
        base_unique_values = column_values.unique().tolist()
        if not base_unique_values:
            
            continue

        print(f"> Column: '{column}'")

        # 3. Compare base unique values against all Column's values
        for base in tqdm(base_unique_values, desc=f" Searching implicit values for: '{column}'"):
            pattern = re.compile(re.escape(base), re.IGNORECASE)

            matches = [val for val in column_values if val != base and pattern.search(val)]

            if matches:
                print(f"  '{base}' → {matches}")

# Function for replacing string date values to datetime values
def replace_string_values_datetime(df, include=None, exclude=None, frmt=None, time_zone='UTC'):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if df[column].dtype != 'object':
            
            continue
        
        else:
            
            df[column] = pd.to_datetime(df[column], format=frmt, errors='coerce')
            
            try:
                
                df[column] = df[column].dt.tz_localize(time_zone)
            
            except TypeError:
                
                df[column] = df[column].dt.tz_convert(time_zone)
    
    return df

# Function for findingv alues ​​that do not allow conversion to numeric
def find_errors_to_numeric(df, column):
    
    mask = pd.to_numeric(df[column], errors='coerce').isna() & df[column].notna()
    non_integer_values = df.loc[mask, column]
    
    if non_integer_values.empty:
        
        pass
   
    else:
        
        print(f"*** Warning ***   > Non numeric values found in column [{column}]:\n{non_integer_values}\n")
        print(f"> Conversion unsuccessful, non numeric values amount: {non_integer_values.shape[0]}\n")
                
    numeric_col = pd.to_numeric(df[column], errors='coerce')
    mask = (numeric_col % 1 != 0) & (~numeric_col.isna())
    non_integer_numeric = df.loc[mask, column]
    
    if non_integer_numeric.empty:
        
        pass
   
    else:
        
        print(f"*** Warning ***   > Numeric values that are not whole integer found in column [{column}]:\n{non_integer_numeric}\n")
        print(f"> Conversion unsuccessful, numeric values non whole integer amount: {non_integer_numeric.shape[0]}\n")

# Function for converting values to integer data type
def convert_ndtype_to_numeric(df, type=None, include=None, exclude=None):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if type == 'integer':
            
            if np.array_equal(df[column], df[column].astype('int')):
                
                df[column] = pd.to_numeric(df[column], downcast='integer', errors="coerce")
            
            else:
                
                find_errors_to_numeric(df, column)                

            
        elif type == 'float':
                
                df[column] = pd.to_numeric(df[column], downcast='float', errors="coerce")
            
        else:
            
            if np.array_equal(df[column], df[column].astype('int')):
                
                df[column] = pd.to_numeric(df[column], errors="coerce")
            
            else:
                
                find_errors_to_numeric(df, columns)    
                
                df[column] = pd.to_numeric(df[column], errors="coerce")
    
    return df

# Function for converting integer values to boolean data type
def convert_integer_to_boolean(df, include=None, exclude=None):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if df[column].dtype != 'int':
            
            continue
        
        else:
            
            df[column] = df[column].astype(bool)
    
    return df


# Function for converting abbreviated gender values to complete gender
def standardize_gender_values(df, include=None, exclude=None):    
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if df[column].dtype != 'object':
            
            continue
        
        else:
            
            df[column] = df[column].replace('f', 'female')
            df[column] = df[column].replace('m', 'male')
    
    return df


    