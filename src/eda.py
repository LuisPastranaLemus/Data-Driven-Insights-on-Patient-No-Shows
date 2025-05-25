# Exploratory Data Analysis for Visualizations and summary statistics

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

# Missing values for identifying and analyzing missing values within a dataframe
def missing_values_heatmap(df):
    
    plt.figure(figsize=(15, 7))
    sns.heatmap(df.isna(), cbar=False, cmap='viridis', yticklabels=False)
    plt.title('Missing values heatmap')
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.tight_layout()
    plt.show()

# Plot a graph for "N" Boxplots one next to the other
# plot_multiple_boxplots_vertical(ds_list=[serie1, serie2, serie3], xlabels=['A', 'B', 'C'], ylabel='Valores',
#                                 title='Title', color=['red', 'green', 'blue'])
def plot_boxplots(ds_list, xlabels, ylabel, title, yticks_range=None, rotation=0, color='grey'):
  
    if len(ds_list) != len(xlabels):
        raise ValueError("*** Error ***   > The data list and labels must be the same length.")
    
    df = pd.DataFrame({'value': pd.concat(ds_list, ignore_index=True),
                       'group': sum([[label]*len(s) for label, s in zip(xlabels, ds_list)], [])})
    
    plt.figure(figsize=(15, 7))

    
    # If color is list, assign custom palette; if string, use solid color
    if isinstance(color, (list, tuple)) and len(color) == len(xlabels):
        palette = dict(zip(xlabels, color))
        sns.boxplot(x='group', y='value', data=df, palette=palette)
    else:
        sns.boxplot(x='group', y='value', data=df, color=color)
    
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=rotation)
    
    if yticks_range is not None:
        plt.ylim(yticks_range[0], yticks_range[1])
    
    plt.yticks(np.arange(*yticks_range), rotation=rotation)
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()


# Plot a Histogram graph
# plot_histogram(ds=series1, bins=np.arange(0, 1475, 25), color='grey', title='Distribution of Monthly Durations',
#                xlabel='Duration (minutes)', ylabel='Frequency', xticks_range=(0, 1500, 50), yticks_range=(0, 80, 8))
def plot_histogram(ds, bins=10, color='grey', title='', xlabel='', ylabel='Frequency', xticks_range=None, yticks_range=None, rotation=0):

    # Make sure no mising values exists
    ds = ds.dropna()
    
    # Media and Mean calculation
    mean_val = ds.mean()
    median_val = ds.median()

    plt.figure(figsize=(15, 7))
    sns.histplot(ds, bins=bins, edgecolor='black', color=color, kde=False)

    # Mean line
    plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
    # Median Line
    plt.axvline(median_val, color='blue', linestyle='dashdot', linewidth=1.5, label=f'Median: {median_val:.2f}')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if xticks_range is not None:
        plt.xlim(xticks_range[0], xticks_range[1])
    if yticks_range is not None:
        plt.ylim(yticks_range[0], yticks_range[1])
    
    plt.xticks(np.arange(*xticks_range), rotation=rotation)
    plt.yticks(np.arange(*yticks_range), rotation=rotation)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Plot a Frequency Density graph
# plot_frequency_density(ds=series1, bins=np.arange(0, 1200, 50), color='grey', title='Frequency density', xlabel='Duration(minutes)',
#                        ylabel='Density', xticks_range=(0, 1200, 100), show_kde=True)
def plot_frequency_density(ds, bins=10, color='grey', title='', xlabel='', ylabel='Density',xticks_range=None, rotation=0, show_kde=True):

    ds = ds.dropna()
    mean_val = ds.mean()
    median_val = ds.median()

    plt.figure(figsize=(15, 7))
    
    # Histogram with density instead of frequency
    sns.histplot(ds, bins=bins, stat='density', edgecolor='black', color=color, alpha=0.7)

    # Optional KDE overlay
    if show_kde:
        sns.kdeplot(ds, color='darkblue', linewidth=2, label='KDE')

    # Mean and Median lines
    plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean: {mean_val:.2f}')
    plt.axvline(median_val, color='blue', linestyle='dashdot', linewidth=1.5, label=f'Median: {median_val:.2f}')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if xticks_range:
        plt.xlim(xticks_range[0], xticks_range[1])

    plt.xticks(np.arange(*xticks_range), rotation=rotation)
    plt.legend()
    plt.grid(True)
        
    plt.tight_layout()
    plt.show()

# Plot a grouped bar plot (3 values X, Y and Hue)
# plot_grouped_barplot(data=dataframe, x_col='month', y_col='median_duration', hue_col='plan', palette=['black', 'grey'], 
#                      title='Average Call', xlabel='Month', ylabel='Average Call Duration (min)', xticks_range=range(0, 13, 1),
#                      yticks_range=range(0, 500, 50), rotation=65)
def plot_grouped_barplot(df, x_col, y_col, hue_col=None, palette=['black', 'grey'], title='', xlabel='', ylabel='', xticks_range=None, 
                         yticks_range=None, rotation=0):

    plt.figure(figsize=(15, 7))
    
    sns.barplot(data=ds, x=x_col, y=y_col, hue=hue_col, palette=palette)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    if xticks_range is not None:
        plt.xticks(range(xticks_range), rotation=rotation)
    if yticks_range is not None:
        plt.yticks(range(yticks_range), rotation=rotation)

    if show_grid:
        plt.grid(True, axis='y', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.show()