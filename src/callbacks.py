from dash import Input, Output, html
import numpy as np
from scipy import stats

from graphs import generate_hist
from data import df

def generate_callbacks(application):
    @application.callback(
    [Output('hist_graph', 'figure'),
     Output('hist_title', 'children'),
     Output('t_test_p', 'children')],
    Input('hist_dd', 'value'))

    def upgrade_hist(a):
        if a:
            if a == 'Fractal Dimension':
                aa = a.lower().replace(' ', '_')
                
            else:
                aa = a.lower()
                
            fig = generate_hist(df = df, x = aa)
            
            title = f'{a} distribution'
            
            num_iterations = 1000
            bts_stat = np.zeros(num_iterations)
            bts_worst = np.zeros(num_iterations)
            
            for i in range(num_iterations):
                bts_stat_sample = np.random.choice(df[df['type'] == 'normal'][aa],
                                                   size = len(df), replace = True)
                bts_worst_sample = np.random.choice(df[df['type'] == 'worst'][aa],
                                                    size = len(df), replace = True)
                
                bts_stat[i] = np.mean(bts_stat_sample)
                bts_worst[i] = np.mean(bts_worst_sample)
                
            t_test_statistic, t_test_pvalue = stats.ttest_ind(bts_stat_sample, bts_worst_sample)
            
        else:
            fig = generate_hist(df = df, x = 'radius')
            title = f'Radius distribution'
            
            bts_stat = np.zeros(num_iterations)
            bts_worst = np.zeros(num_iterations)
            
            for i in range(num_iterations):
                bts_stat_sample = np.random.choice(df[df['type'] == 'normal']['radius'],
                size = len(df), replace = True)
                bts_worst_sample = np.random.choice(df[df['type'] == 'normal']['worst'],
                                                    size = len(df), replace = True)
                
                bts_stat[i] = np.mean(bts_stat_sample)
                bts_worst[i] = np.mean(bts_worst_sample)
                
            t_test_statistic, t_test_pvalue = stats.ttest_ind(bts_stat_sample, bts_worst_sample)
            
        if t_test_pvalue < .05:
            p_children = [html.Strong(id = 'p_t_test_positive', children = 'Null Hypothesis Rejected'),
                          html.Br(),
                          f'Statistic value: {t_test_statistic}',
                          html.Br(),
                          f'p-value: {t_test_pvalue}']
            
        else:
            p_children = [html.Strong(id = 'p_t_test_negative', children = 'Failed to Reject Null Hypothesis'),
                          html.Br(),
                          f'Statistic value: {t_test_statistic}',
                          html.Br(),
                          f'p-value: {t_test_pvalue}']
            
        return fig, title, p_children