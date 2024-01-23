import dash
from dash import Input, Output

from graphs import generate_hist
from data import df

def generate_callbacks(application):
    @application.callback(
    [Output('hist_graph', 'figure'),
     Output('hist_graph_worst', 'figure'),
     Output('regular_title', 'children'),
     Output('worst_title', 'children')],
    Input('hist_dd', 'value'))

    def upgrade_hist(a):
        if a:
            if a == 'Fractal Dimension':
                a_stat = a.lower().replace(' ', '_') + '_mean'
                a_worst = a.lower().replace(' ', '_') + '_worst'
                
            else:
                a_stat = a.lower() + '_mean'
                a_worst = a.lower() + '_worst'
                
            fig_1 = generate_hist(df = df, x = a_stat)
            fig_2 = generate_hist(df = df, x = a_worst)
            
            reg = f'Regular {a}'
            worst = f'Worst {a}'
            
        else:
            fig_1 = generate_hist(df = df, x = df['radius_mean'])
            fig_2 = generate_hist(df = df, x = df['radius_worst'])
            reg = f'Regular Radius'
            worst = f'Worst Radius'
            
        return fig_1, fig_2, reg, worst