import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table

from data import variables, df
from callbacks import generate_callbacks
from functions import generate_knn_line
from knn import selected_columns
from misc import model_p

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

app.layout = html.Div(id = 'home_div', children = [
    html.Meta(name='viewport', content='width=device-width, initial-scale=1'),
    dbc.Row(id = 'title_row' , children = [
        dbc.Col(id = 'title', children = 
            html.H2('BREAST CANCER TUMOR ANALYSIS')),
        dbc.Col(id = 'dropdown', children = [
            html.H6(id = 'dropdown_text', children = 'SELECT A VARIABLE'),
            dcc.Dropdown(id = 'hist_dd', options = variables, value = 'Radius')])]),
    dbc.Row(children = [
        dbc.Row(id = 'subtitles_row_s', children = html.H4(id = 'hist_title')),
        dbc.Row(id = 'stats_row', children = [
            dbc.Card(id = 'hist_graph_card', children =
                dcc.Graph(id = 'hist_graph')),
            dbc.Col(id = 'stats_col_test', children = [
                html.H5(id = 'levene_title', children = 'EQUALITY OF VARIANCES'),
                html.P(id = 'levene_p'),
                html.H5(id = 'ttest_title', children = 'INDEPENDENT SAMPLES T TEST'),
                html.P(id = 'ttest_p')]),
            dbc.Col(id = 'stats_col_descriptive', children = [
                    html.H5(id = 'descriptive_title', children = 'DESCRIPTIVE STATISTICS'),
                    dbc.Row(html.P(id = 'descriptive_p_normal')),
                    dbc.Row(html.P(id = 'descriptive_p_worst'))])])]),
    dbc.Row([
        dbc.Row(id = 'subtitles_row_k', children = html.H4('K-NEIGHBORS CLASSIFICATION MODEL')),
        dbc.Row([
            dbc.Card(
                dcc.Graph(figure = generate_knn_line(df, selected_columns, 'diagnosis', 15))),
            dbc.Col([
                dbc.Row([
                    dbc.Col(id = 'diagnosis_col'),
                    dbc.Col(id = 'model_input_col', children = [
                        dcc.Input(
                            id = 'perimeter_input',
                            type = 'number',
                            debounce = True,
                            placeholder = 'Perimeter value 0 - 500.0',
                            max = 500.0,
                            step = .1),
                        html.Button('PREDICT DIAGNOSIS', id = 'perimeter_button')]),
                    dbc.Col(html.P(id = 'model_p', children = model_p))]),
                dbc.Row(id = 'table_row', children =
                    dash_table.DataTable(id = 'table',
                                         data = df.to_dict('records'),
                                         columns = [{
                                             'name':i.title().replace('_', ' '),
                                             'id':i,
                                             'deletable':True}
                                                    for i in df.columns],
                                         sort_action = 'native',
                                         filter_action = 'native',
                                         style_as_list_view = True,
                                         style_cell= {
                                             'minWidth': '150px',
                                             'width': '150px',
                                             'maxWidth': '150px'},
                                         style_table = {'overflowX':'auto'},
                                         style_header = {'backgroundColor': '#47A992'},
                                         page_size = 6))],
                    width = 6)])])
    ])

generate_callbacks(app)

server = app.server

if __name__ == '__main__':
    app.run(debug = False)