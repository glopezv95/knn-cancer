import plotly.express as px
import pandas as pd

from data import df, df_stats, df_stats_worst

def generate_hist(df: pd.DataFrame, x: str):
    fig = px.histogram(
        data_frame = df,
        x = x)
    
    fig.update_layout(xaxis_title = '',
                      yaxis_title = '',
                      showlegend = False,
                      plot_bgcolor = 'rgb(0,0,0)',
                      paper_bgcolor = 'rgb(0,0,0)')
    
    return fig