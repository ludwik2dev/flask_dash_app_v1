from dash import Dash, html, dcc, callback, Output, Input,State
import plotly.graph_objects as go
import pandas as pd


app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title - My first App'),
    
    html.Div([
        html.Div(dcc.Dropdown(id='dropdown-selection'), style={'width': '50%', 'marginRight': '10px'}),
        html.H3(id='dropdown-label', style={'width': '50%', 'marginLeft': '10px'}),
    ], style={'display': 'flex', 'alignItems': 'center'}),

    dcc.Input(id="year-from-input", type="number", placeholder="Year from"),  # , debounce=True
    dcc.Input(value=2023, id="year-to-input", type="number", placeholder="Year to"),
    
    dcc.Graph(id='graph-content'),

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

    df = pd.DataFrame.from_dict(store)
    df_ = df[(df['country'] == country) & (df['year'] >= year_from) & (df['year'] <= year_to)]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_['year'], 
            y=df_['pop'],
            line={'color': 'black'},
            marker={'color': 'red'},
            mode='lines+markers'
        )
    )
    fig.update_layout(
        plot_bgcolor='lightgreen',
    )

    label = f'User selected: {country}'

    return fig, label


if __name__ == '__main__':
    app.run(debug=True)