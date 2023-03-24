import dash
from dash import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from src.dash_client.html.layout import layout
from src.dash_client.api_request.api_request import ApiRequest
from src.dash_client.dataframe.dataframe import Data

df = Data(ApiRequest().get_data(1), ApiRequest().get_data(3))

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = layout(df)


@app.callback(
    Output('hist-type-chart', 'figure'),
    Input('color', 'value'),
    Input('x-column', 'value')
)
def update_hist(color, x_column):
    if color == 'All':
        histogram = px.histogram(df.df, x=x_column, color="Target")
    elif color and x_column:
        histogram = px.histogram(df.df.loc[df.df['Target'] == int(color)], x=x_column, color="Target")

    return histogram


@app.callback(
    Output('scatter-temp-chart', 'figure'),
    Input('x-column-scatter', 'value'),
    Input('y-column-scatter', 'value')
)
def update_scatter(x_column, y_column):
    scatter = px.scatter(df.df, x=x_column, y=y_column)
    return scatter


@app.callback(
    Output('hist-all-chart', 'figure'),
    Input('x-column-hist', 'value')
)
def update_hist_all(x_column):
    histogram_all = px.histogram(df.df, x=x_column)

    return histogram_all


@app.callback(Output('tbl_out', 'children'), Input('data_tbl', 'active_cell'), Input('data_tbl', 'page_current'))
def update_graphs(active_cell, page_current):
    id_row = None
    if active_cell and page_current:
        id_row = page_current * 8 + active_cell['row']
    elif active_cell:
        id_row = active_cell['row']

    return df.df_prediction['Predict Target'].iloc[[id_row]] if id_row else 'Select row'
