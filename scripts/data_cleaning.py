# data_cleaning.py for dataset cleaning

from tqdm import tqdm
import re

def check_existing_missing_values(df, df_name="DataFrame"):
    
    missing_values = ['', ' ', 'N/A', 'none', 'None', 'null', 'NULL', 'NaN', 'nan', 'NAN', 'nat', 'NaT']
    
    print(f"Dataframe: {df_name}")
    
    for column in df.columns:
    
        if df[column].isin(missing_values).any():
        
            print(f"Mising values in '{column}': {df[column].isin(missing_values).sum()}")
        
        else:
            
            print(f"No missing values in '{column}' found")

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
    
        if df[column].isin(missing_values).any():
        
            df[column] = df[column].replace(missing_values, pd.NA)

    return df

# Function for format normalizing type 'object' (strings)
def normalize_string_format(df, include=None, exclude=None):
    
    specialChars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '{', '}', '[', ']', '|', '\\', ':', ';', '"', 
                    "'", '<', '>', ',', '.', '?', '/', '~', '`','°', '¬', '¦', '¢', '£', '¤', '¥', '§', '©', 'ª', '«', '®', '¯', '°', '±', 
                    '²', '³', '´', 'µ', '¶', '·', '¸', '¹', 'º', '»', '¼', '½', '¾', '¿', '×', '÷', '¡', '¿'] 
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
       if df[column].dtype == 'object':
           
           for spec_char in specialChars:
               
               df[column] = df[column].str.replace(spec_char, '')
        
           df[column] = df[column].str.replace(' ', '_')
           df[column] = df[column].str.replace(r'__+', '_', regex=True)
           df[column] = df[column].str.lower()
           df[column] = df[column].str.strip()
        
       else:
           
           continue
    
    return df

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

        print(f"\nColumn: '{column}'")

        # 3. Compare base unique values against all Column's values
        for base in tqdm(base_unique_values, desc=f"Searching implicit values for: '{column}'"):
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
        
        df[column] = pd.to_datetime(df[column], format=frmt, errors='coerce')
        
        try:
            
            df[column] = df[column].dt.tz_localize(time_zone)
        
        except TypeError:
            
            df[column] = df[column].dt.tz_convert(time_zone)
    
    return df