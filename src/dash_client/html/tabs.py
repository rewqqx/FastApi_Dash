from dash import dcc, html
import dash_bootstrap_components as dbc
from dash import dash_table
import numpy as np
import plotly.express as px
from sklearn.metrics import confusion_matrix
import joblib
from src.dash_client.api_request.api_request import ApiRequest


def tab_df_content(df):
    histogram = px.histogram(df.df, x="Air temperature [K]", color="Target", title='Frequency histogram')

    scatter = px.scatter(df.df, x="Air temperature [K]", y="Air temperature [K]", title='Scatter Plot')

    histogram_all = px.histogram(df.df, x="Air temperature [K]", title='Frequency histogram')

    pie = px.pie(df.df, values="Air temperature [K]", names="Type", color="Type", title='Pie plot with Type')

    tab = [dbc.Row([
        dbc.Col([
            html.Div([
                html.Div('Select Variable'),
                dcc.Dropdown(
                    df.features,
                    'Air temperature [K]',
                    id='x-column-hist',
                    clearable=False
                )
            ]),
        ], width={'size': 2}),
        dbc.Col([
            html.Div([
                html.Div('Set X'),
                dcc.Dropdown(
                    df.features,
                    'Air temperature [K]',
                    id='x-column-scatter',
                    clearable=False
                )
            ])
        ], width={'size': 2, 'offset': 4}),
        dbc.Col([
            html.Div([
                html.Div('Set Y'),
                dcc.Dropdown(
                    df.features,
                    'Air temperature [K]',
                    id='y-column-scatter',
                    clearable=False
                )
            ])
        ], width={'size': 2})
    ], style={'margin-top': '25px', 'margin-left': 10}),

        dbc.Row([
            dbc.Col([dcc.Graph(id='hist-all-chart',
                               figure=histogram_all),
                     ], width={'size': 6}),
            dbc.Col([
                dcc.Graph(id='scatter-temp-chart',
                          figure=scatter),
            ], width={'size': 6})
        ], style={'margin-left': 10}),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div('Select Type'),
                    dcc.Dropdown(
                        np.append(df.df['Target'].unique(), 'All'),
                        'All',
                        id='color',
                        clearable=False
                    )
                ]),
            ], width={'size': 1}),
            dbc.Col([
                html.Div([
                    html.Div('Select Variable'),
                    dcc.Dropdown(
                        df.features,
                        'Air temperature [K]',
                        id='x-column',
                        clearable=False
                    )
                ])
            ], width={'size': 2}),
        ], style={'margin-left': 10}),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='hist-type-chart',
                          figure=histogram),
            ], width={'size': 6}),
            dbc.Col([
                dcc.Graph(id='pie-chart',
                          figure=pie),
            ])
        ])
    ]

    return tab


def tab_model_content(df):
    ApiRequest().save_model()
    model = joblib.load('../files/dash/model.csv')

    model_bar = px.bar(x=model.feature_importances_, y=model.feature_names_in_,
                       labels={'x': 'Importance', 'y': 'Feature'}, title='Feature Importance')

    cf = confusion_matrix(df.df_prediction['Target'], df.df_prediction['Predict Target'], labels=[0, 1])

    cm = px.imshow(cf, text_auto=True, x=['0', '1'], y=['0', '1'], title='Confusion Matrix',
                   labels={'x': 'True class', 'y': 'Predicted class'})

    tab = [
        dbc.Row([
            dbc.Col([
                html.Div(['Data Table']),
                dash_table.DataTable(df.df.to_dict('records'), [{"name": i, "id": i} for i in df.df.columns],
                                     page_size=8,
                                     style_table={'overflowY': 'auto', 'margin-top': '35px'},
                                     style_cell={'width': 100}, id='data_tbl'), dbc.Alert(id='tbl_out')
            ], width=6),
            dbc.Col([
                dcc.Graph(id='model-cm',
                          figure=cm),
            ], width=6)
        ], style={'margin-top': '25px', 'margin-left': 10}
        ),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='model-bar',
                          figure=model_bar),
            ], width=6)
        ], style={'margin-top': '25px', 'margin-left': 10})
    ]

    return tab
