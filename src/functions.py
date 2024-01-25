import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import itertools
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def generate_hist(df: pd.DataFrame, x: str):
    
    fig = px.histogram(
        data_frame = df,
        x = x,
        color = 'type',
        barmode = 'overlay',
        marginal = 'box',
        color_discrete_sequence = ['#47A992', '#482121'])
    
    fig.update_layout(
        margin=dict(l=20, r=20, b=20, t=20),
        legend_title = '',
        xaxis_title = '',
        yaxis_title = '',
        plot_bgcolor = '#F5F7F8',
        paper_bgcolor = '#F5F7F8',
        legend = dict(
            font = dict(family = 'Segoe UI',
                        size = 14)))
    
    return fig

def bootstrap_means_dist(data: pd.DataFrame, iterations:int, contrast_column: str,
                         filter: str):
    
    np.random.seed(17)
    bootstrap_means_dict = {_:np.zeros(iterations) for _ in data[contrast_column].unique()}
    
    for condition in data[contrast_column].unique():
        for i in range(iterations):
            bootstrap_dist = np.random.choice(
                data[data[contrast_column] == condition][filter],
                size = len(data),
                replace = True)
            
            bootstrap_means_dict[condition][i] = np.mean(bootstrap_dist)
            
    return bootstrap_means_dict

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

def generate_diagnosis(dataframe: pd.DataFrame, value, X: str, y: str, k: int):
    array_X = np.array(dataframe[X].values.reshape(-1, 1))
    knn = KNeighborsClassifier(n_neighbors = k)
    
    knn.fit(array_X, dataframe[y].values.astype(str))
    diagnosis = knn.predict(np.array(value).reshape(-1, 1))
    
    return diagnosis

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
    
    fig = go.Figure(go.Scatter(
        x = neighbors,
        y = list(test_scores.values()),
        hovertemplate =
        '<b>Accuracy:</b> %{y:.3f}'+
        '<br><b>k</b>: %{x}',
        name = 'test accuracy',
        mode = 'lines',
        line = dict(color = '#47A992')))
    
    fig.add_trace(go.Scatter(
        x = neighbors,
        y = list(train_scores.values()),
        hovertemplate =
        '<b>Accuracy:</b> %{y:.3f}'+
        '<br><b>k</b>: %{x}',
        name = 'train accuracy',
        mode = 'lines',
        line = dict(color = '#482121')))
    
    fig.update_layout(
        margin=dict(l=20, r=20, b=20, t=20),
        legend_title = '',
        xaxis_title='',
        yaxis_title='',
        hovermode = 'x',
        plot_bgcolor = '#F5F7F8',
        paper_bgcolor = '#F5F7F8',
        legend = dict(
            font = dict(family = 'Segoe UI',
                        size = 14)))
    
    # fig.for_each_trace(
    #     lambda t: t.update(name='Testing accuracy') if t.name == 'trace 0' else None)
    # fig.for_each_trace(
    #     lambda t: t.update(name='Train accuracy') if t.name == 'trace 1' else None)

    return fig