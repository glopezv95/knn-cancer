import plotly.express as px
import pandas as pd

def generate_hist(df: pd.DataFrame, x: str):
    
    fig = px.histogram(data_frame = df,
                       x = x,
                       color = 'type',
                       barmode = 'overlay',
                       marginal = 'box')
    
    fig.update_layout(xaxis_title = '',
                      yaxis_title = '',
                      plot_bgcolor = 'rgb(0,0,0)',
                      paper_bgcolor = 'rgb(0,0,0)')
    
    return fig