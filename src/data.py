import os
import pandas as pd

abs_path = os.path.dirname(__file__)
df_path = os.path.join(abs_path, '..\\data\\data.csv')

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