from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)
server = app.server

df = pd.read_excel('deathdata.xls')

app.layout = html.Div(children=[
    dcc.Dropdown(df['Субъект'].unique(), 'Российская Федерация', id='state-dropdown'),
    dcc.Dropdown(df['Пол'].unique(), 'Оба пола', id='sex-dropdown'),
    html.Div(
        dcc.Graph(id='graph')
    ),

    dcc.RangeSlider(df['Год'].min(),
                    df['Год'].max(),
                    step=None,
                    value=[df['Год'].min(), df['Год'].max()],
                    id='slider',
                    marks={str(year): str(year) for year in df['Год'].unique()}
                    )
])


@app.callback(
    Output('graph', 'figure'),
    [Input('state-dropdown', 'value'),
     Input('sex-dropdown', 'value'),
     Input('slider', 'value')])
def update_graph(state_value, sex_value, year_value):
    dff = df[(df['Субъект'] == state_value) &
             (df['Пол'] == sex_value) &
             ((df['Год'] >= year_value[0]) & (df['Год'] <= year_value[1]))]
    dff = dff.sort_values(by=['Год', 'Возраст'])
    fig = px.bar(dff,
                 x='Возраст',
                 y='Число умерших',
                 color='Год',
                 )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
