import os
import pandas as pd
import plotly.express as px

# Get path of data.csv
abs_path = os.path.dirname(__file__)
df_path = os.path.join(abs_path, '..\\data\\data.csv')

# Import data.csv and apply data cleaning and classification
df = pd.read_csv(df_path)

df = df[['diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean',
       'area_mean', 'smoothness_mean', 'compactness_mean',
       'concavity_mean', 'symmetry_mean', 'fractal_dimension_mean',
       'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
       'smoothness_worst', 'compactness_worst', 'concavity_worst',
       'symmetry_worst', 'fractal_dimension_worst']]

df_stats_worst = []
df_stats = []

for column in df.columns.drop('diagnosis'):
    if column.endswith('worst'):
        df_stats_worst.append(column)
    else:        
        df_stats.append(column)
        
variables = []

for column in df_stats:
    variables.append(column[:-5].title().replace('_', ' '))

# Reorganize data according to quality of tumor    
df_worst = df.drop(df_stats, axis = 1)
df_best = df.drop(df_stats_worst, axis = 1)

for column in df_worst.columns.drop('diagnosis'):
    df_worst.rename({column:column[:-6]}, axis = 1, inplace = True)
    
for column in df_best.columns.drop('diagnosis'):
    df_best.rename({column:column[:-5]}, axis = 1, inplace = True)

df_worst['type'] = 'worst'
df_best['type'] = 'normal'

df = pd.concat([df_best, df_worst], ignore_index = True)

# Set up categorical data 'diagnosis' for machine learning knn model
df.loc[df['diagnosis'] == 'M', 'diagnosis'] = 1
df.loc[df['diagnosis'] == 'B', 'diagnosis'] = 0