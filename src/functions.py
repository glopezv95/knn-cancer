import plotly.express as px
import pandas as pd
import itertools
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

from data import df

def generate_hist(df: pd.DataFrame, x: str):
    
    fig = px.histogram(
        data_frame = df,
        x = x,
        color = 'type',
        barmode = 'overlay',
        marginal = 'box')
    
    fig.update_layout(
        margin=dict(l=20, r=20, b=20, t=20),
        xaxis_title = '',
        yaxis_title = '',
        plot_bgcolor = 'rgb(0,0,0)',
        paper_bgcolor = 'rgb(0,0,0)')
    
    return fig

def test_knn(dataframe: pd.DataFrame, drop_columns: list, y: str, n_columns: int, max_k):
    best_dict = {}
    feature_columns = dataframe.columns.drop(drop_columns)
    dataframe[y] = dataframe[y].astype(str)

    best_accuracy = 0.0

    for combination in itertools.combinations(feature_columns, n_columns):
        X = np.array(dataframe[list(combination)].values)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            dataframe[y].values,
            test_size = .3,
            random_state = 17,
            stratify = dataframe[y].values)
        
        for i in range(1, max_k + 1):

            knn = KNeighborsClassifier(n_neighbors=i)
            knn.fit(X_train, y_train)

            accuracy = knn.score(X_test, y_test)

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_dict['best_accuracy'] = accuracy
                best_dict['best_combination'] = combination
                best_dict['best_k'] = i
                
    return best_dict

def generate_knn_line(dataframe: pd.DataFrame, X: list, y: str, max_k):
    neighbors = np.arange(1, max_k + 1)
    test_scores = {}
    train_scores = {}
    dataframe[y] = dataframe[y].astype(str)
    
    if len(X) == 1:
        X = dataframe[X].values.reshape(-1, 1)
    
    else:
        X = dataframe[X].values
        
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        dataframe[y].values,
        test_size = .3,
        random_state = 17,
        stratify = dataframe[y].values)
        
    for neighbor in neighbors:
        knn = KNeighborsClassifier(n_neighbors = neighbor)
        
        knn.fit(X_train, y_train)
        
        test_scores[neighbor] = knn.score(X_test, y_test)
        train_scores[neighbor] = knn.score(X_train, y_train)
        
    fig = px.line(
        data_frame = dataframe,
        x = neighbors,
        y = [test_scores.values(), train_scores.values()])
    
    fig.update_layout(
        margin=dict(l=20, r=20, b=20, t=20),
        xaxis_title='',
        yaxis_title='')
    
    fig.for_each_trace(lambda t: t.update(name='Testing accuracy') if t.name == 'wide_variable_0' else None)
    fig.for_each_trace(lambda t: t.update(name='Train accuracy') if t.name == 'wide_variable_1' else None)

    
    return fig