# __init__.py is a special file Python looks for when treating a folder as a package.

# Smart __init__.py used for importing easily from the package.

try:
    
    from .data_loader import (load_dataset_from_zip, 
                              load_dataset_from_csv, 
                              load_dataset_from_excel, 
                              load_dataset_from_list, 
                              load_dataset_from_dict)
    
    from .data_cleaning import (check_existing_missing_values,
                                replace_missing_values,
                                normalize_string_format,
                                detect_implicit_duplicates,
                                replace_string_values_datetime)
    
    from .eda import (missing_values_heatmap,
                      plot_boxplots,
                      plot_histogram,
                      plot_frequency_density,
                      plot_grouped_barplot)
                      

except ImportError as e:
    raise ImportError("One or more modules could not be found."
                      "Ensure required scripts exist in the same directory as '__init__.py'.") from e

__all__ = ['load_dataset_from_zip', 
           'load_dataset_from_csv', 
           'load_dataset_from_excel', 
           'load_dataset_from_list', 
           'load_dataset_from_dict',
           
           'check_existing_missing_values',
           'replace_missing_values',
           'normalize_string_format',
           'detect_implicit_duplicates',
           'replace_string_values_datetime',
           
           'missing_values_heatmap',
           'plot_boxplots',
           'plot_histogram',
           'plot_frequency_density',
           'plot_grouped_barplot']