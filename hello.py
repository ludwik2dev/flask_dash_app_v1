from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objects as go
import pandas as pd


df = pd.read_csv('gapminder.csv')
counries = df['country'].unique()


app = Dash(__name__)


app.layout = html.Div([
    html.H1(children='Title - My first App'),
    dcc.Dropdown(options=counries, value='Poland', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
])

@callback(
    Output(component_id='graph-content', component_property='figure'),
    Input(component_id='dropdown-selection', component_property='value'),
)
def update_graph(value):
    print(value)
    df_ = df[df['country'] == value]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_['year'], 
            y=df_['pop'],
        )
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, dev_tools_hot_reload=True)