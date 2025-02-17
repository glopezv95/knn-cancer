import pandas as pd
from dash import Input, Output, html, no_update
from dash import callback_context as ctx
import numpy as np
from scipy import stats

from functions import generate_hist, bootstrap_means_dist, generate_diagnosis
from data import df
from knn import selected_k

def generate_callbacks(application):
    @application.callback(
    [Output('hist_title', 'children'),
     Output('hist_graph', 'figure'),
     Output('levene_p', 'children'),
     Output('ttest_p', 'children')],
    Input('hist_dd', 'value'))

    def test_distribution(a):
        aa = 'radius'
                
        if a:
            aa = a.lower().replace(' ', '_')
              
        title = f'{aa.upper().replace("_", " ")} DISTRIBUTION (CASE SCENARIOS)'
        fig = generate_hist(df = df, x = aa)
        
        bts_normal = bootstrap_means_dist(df, 1000, 'type', aa)['normal']
        bts_worst = bootstrap_means_dist(df, 1000, 'type', aa)['worst']
            
        levene_statistic, levene_pvalue = stats.levene(bts_normal, bts_worst)
            
        if levene_pvalue < .05:
            levene_p = [html.Strong(id = 'p_levene_positive',
                                    children = 'Null Hypothesis Rejected',
                                    style = dict(color = '#7A3E3E')),
                          html.Br(),
                          f"{aa.title().replace('_', ' ')} normal and worst case scenarios",
                          html.P("have significantly different variance"),
                          f'Statistic value: {levene_statistic}',
                          html.Br(),
                          f'p-value: {levene_pvalue}']
            
            ttest_statistic, ttest_pvalue = stats.ttest_ind(bts_normal, bts_worst,
                                                            equal_var = False)
            
            if ttest_pvalue < .05:
                ttest_p = [html.Strong(id = 'p_ttest_positive',
                                       children = 'Null Hypothesis Rejected',
                                       style = dict(color = '#7A3E3E')),
                           html.Br(),
                           f"{aa.title().replace('_', ' ')} normal and worst case scenarios",
                           html.P("have significantly different means"),
                           f'Statistic value: {ttest_statistic}',
                           html.Br(),
                           f'p-value: {ttest_pvalue}']
            
            else:
                ttest_p = [html.Strong(id = 'p_ttest_negative',
                                       children = 'Failed to Reject Null Hypothesis',
                                       style = dict(color = '#47A992')),
                            html.Br(),
                            f"{aa.title().replace('_', ' ')} normal and worst case scenarios",
                            html.P("don't have significantly different means"),
                            f'Statistic value: {ttest_statistic}',
                            html.Br(),
                            f'p-value: {ttest_pvalue}']
            
        else:
            levene_p = [html.Strong(id = 'p_levene_negative',
                                    children = 'Failed to Reject Null Hypothesis',
                                    style = dict(color = '#47A992')),
                          html.Br(),
                          f"{aa.title().replace('_', ' ')} normal and worst case scenarios",
                          html.P("don't have significantly different variance"),
                          f'Statistic value: {levene_statistic}',
                          html.Br(),
                          f'p-value: {levene_pvalue}']
            
            ttest_statistic, ttest_pvalue = stats.ttest_ind(bts_normal, bts_worst,
                                                            equal_var = True)
            
            if ttest_pvalue < .05:
                ttest_p = [html.Strong(id = 'p_ttest_positive',
                                       children = 'Null Hypothesis Rejected',
                                       style = dict(color = '#7A3E3E')),
                            html.Br(),
                            f"{aa.title().replace('_', ' ')} normal and worst case scenarios",
                            html.P("have significantly different means"),
                            f'Statistic value: {ttest_statistic}',
                            html.Br(),
                            f'p-value: {ttest_pvalue}']
            
            else:
                ttest_p = [html.Strong(id = 'p_ttest_negative',
                                       children = 'Failed to Reject Null Hypothesis',
                                       style = dict(color = '#47A992')),
                            html.Br(),
                            f"{aa.title().replace('_', ' ')} normal and worst case scenarios",
                            html.P("don't have significantly different means"),
                            f'Statistic value: {ttest_statistic}',
                            html.Br(),
                            f'p-value: {ttest_pvalue}']
            
        return title, fig, levene_p, ttest_p
    
    @application.callback(
        [Output('descriptive_p_normal', 'children'),
        Output('descriptive_p_worst', 'children')],
        Input('hist_dd', 'value'))
    
    def generate_descriptive_statistics(a):
        aa = 'radius'
                
        if a:
            aa = a.lower().replace(' ', '_')
            
        stats_dict = {}
        for item in ['normal', 'worst']:
            stats_dict[item]= {'mean' : np.mean(df[df['type'] == item][aa]),
                               'std' : np.std(df[df['type'] == item][aa]),
                               'count' : len(df[df['type'] == item][aa])}
            
        p_normal = [html.Strong(id = 'title_normal_stats',
                        children = 'Normal cases'),
                    html.Br(),
                    f'Sample mean: {round(stats_dict["normal"]["mean"], 2)}',
                    html.Br(),
                    f'Sample standard deviation: {round(stats_dict["normal"]["std"], 2)}',
                    html.Br(),
                    html.P(f'Sample count: {stats_dict["normal"]["count"]}')]
        
        p_worst = [html.Strong(id = 'title_worst_stats',
                        children = 'Worst cases'),
                   html.Br(),
                   f'Sample mean: {round(stats_dict["worst"]["mean"], 2)}',
                   html.Br(),
                   f'Sample standard deviation: {round(stats_dict["worst"]["std"], 2)}',
                   html.Br(),
                   f'Sample count: {stats_dict["worst"]["count"]}']
        
        return p_normal, p_worst
    
    @application.callback(
        Output('diagnosis_col', 'children'),
        [Input('perimeter_input', 'value'),
         Input('perimeter_button', 'n_clicks')])
    
    def diagnose(input_val, click):
        try:
            diagnosis = None
            
            if ctx.triggered_id == 'perimeter_button' or ctx.triggered_id == 'perimeter_input':
                x = generate_diagnosis(
                    dataframe = df,
                    value = input_val,
                    X = 'perimeter',
                    y = 'diagnosis',
                    k = selected_k)
                
                if int(x[0]) == 1:
                    diagnosis = html.Strong(id = 'diagnosis_p',
                                            children = 'MALIGN',
                                            style = dict(color = '#7A3E3E'))
                else:
                    diagnosis = html.Strong(id = 'diagnosis_p',
                                            children = 'BENIGN',
                                            style = dict(color = '#47A992'))
                       
            return diagnosis
        
        except ValueError as ve:
            if "Input X contains NaN" in str(ve):
                return None