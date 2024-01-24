import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

from data import variables
from callbacks import generate_callbacks
app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])  

app.layout = dbc.Container(children = [
    dbc.Row(
        dcc.Dropdown(id = 'hist_dd', options = variables, value = 'Radius')),
    dbc.Row(children = [
        dbc.Col([
            html.H3(id = 'hist_title'),
            dcc.Graph(id = 'hist_graph')], width = 8),
        dbc.Col([
            html.H3(id = 'levene_title', children = 'Equality of variances test'),
            html.P(id = 'levene_p'),
            html.H3(id = 'ttest_title', children = 'Independent samples t test'),
            html.P(id = 'ttest_p')], width = 4)]),
    dbc.Row([
        html.H3(id = 'descriptive_title', children = 'Descriptive statistics'),
        dbc.Col(html.P(id = 'descriptive_p_normal'), width = 4),
        dbc.Col(html.P(id = 'descriptive_p_worst'), width = 4)])])

generate_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug = True)