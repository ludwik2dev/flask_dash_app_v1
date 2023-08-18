from dash import Dash, html, dcc, callback, Output, Input,State, no_update, ctx
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import pandas as pd
import json


app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title - My first App'),
    
    html.Div([
        html.Div(dcc.Dropdown(id='dropdown-selection'), style={'width': '50%', 'marginRight': '10px'}),
        html.H3(id='dropdown-label', style={'width': '50%', 'marginLeft': '10px'}),
    ], style={'display': 'flex', 'alignItems': 'center'}),

    dcc.Input(value=1950, id="year-from-input", type="text", placeholder="Year from"),  # , debounce=True
    dcc.Input(value=2023, id="year-to-input", type="number", placeholder="Year to"),
    
    dcc.Graph(id='graph-content'),

    html.Div(id='graph-click'),

    dcc.Store(id='store-data'),

], style={'paddingLeft': '200px', 'paddingRight': '200px'}, id='id-layout')


@callback(
    Output('store-data', 'data'),
    Input('id-layout', 'id'),
)
def update_state(_id):
    
    df = pd.read_csv('gapminder.csv')
    return df.to_dict()


@callback(
    Output('dropdown-selection', 'options'),
    Output('dropdown-selection', 'value'),
    Input('store-data', 'data'),
    prevent_initial_call=True
)
def update_dropdown(store):
    
    df = pd.DataFrame.from_dict(store)
    counries = df['country'].unique()
    country = 'Poland'

    return counries, country


@callback(
    Output('graph-content', 'figure'),
    Output('dropdown-label', 'children'),
    Input('dropdown-selection', 'value'),
    Input('year-from-input', 'value'),
    State('year-to-input', 'value'),
    State('store-data', 'data'),
    prevent_initial_call=True
)
def update_graph(country, year_from, year_to, store):

    button_id = ctx.triggered_id 

    if button_id == 'dropdown-selection':
        label = f'User selected: {country}'
    else:
        label = f'User inserted: {year_from}'

    try:
        year_from = int(year_from)
        df = pd.DataFrame.from_dict(store)
        df_ = df[(df['country'] == country) & (df['year'] >= year_from) & (df['year'] <= year_to)]
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df_['year'], 
                y=df_['pop'],
                line={'color': 'black'},
                marker={'color': 'red'},
                mode='lines+markers',
                
            )
        )
        fig.update_layout(
            plot_bgcolor='lightgreen',
            clickmode='event'
        )

        return fig, label

    except ValueError as e:
        print(e)
        return no_update, label


@callback(
    Output('graph-click', 'children'),
    Input('graph-content', 'clickData'),
    prevent_initial_call=True
)
def get_point(clickData):

    print(clickData)
    year = clickData['points'][0]['x']
    pop = clickData['points'][0]['y'] / 1_000_000
    text = f'Year: {year}, population: {round(pop, 2)} mln'
    return text


if __name__ == '__main__':
    app.run(debug=True)