from dash import html
import dash_bootstrap_components as dbc
from src.dash_client.html.tabs import tab_model_content, tab_df_content


def layout(df):
    tab_df = tab_df_content(df)
    tab_model = tab_model_content(df)
    dash_layout = html.Div([
        dbc.Row(html.H1('App Dash'),
                style={'margin-bottom': 50, 'margin-top': 10, 'margin-left': 10}),

        dbc.Tabs([
            dbc.Tab(tab_df, label='Data Content'),
            dbc.Tab(tab_model, label='Model')
        ])
    ])

    return dash_layout
