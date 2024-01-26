from dash import html

from knn import selected_k, selected_columns, selected_accuracy

model_p = [html.Strong('Accuracy: '), f'{selected_accuracy}', html.Br(),
           html.Strong('Features: ')]

for column in selected_columns:
    model_p.append(f'{column.title()}, ')
        
model_p[-1] = model_p[-1].strip(', ')
for item in [html.Br(), html.Strong('Neighbors (k): '), f'{selected_k}']:
    model_p.append(item)