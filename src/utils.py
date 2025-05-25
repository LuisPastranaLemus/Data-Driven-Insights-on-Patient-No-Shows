# utils.py for useful functions

import pandas as pd

def format_notebook():
    
    pd.set_option('display.max_rows', 25) # show maximum 25 rows
    pd.set_option('display.max_columns', 25) # show maximum 10 columns
    pd.set_option('display.max_colwidth', 50) # show maximum 15 characters in each column
    pd.set_option('display.width', 150) # Mostrar 150 caracteres como máximo