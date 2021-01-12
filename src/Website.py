import dash
import os

import dash_core_components as dcc
import dash_html_components as html

github_path = "https://raw.githubusercontent.com/KamWithK/GameRec/11208ae2c94d5b22dc0d5a4fc00fcd38f8d9255a/Data/Images/"
image_paths = [github_path + image for image in os.listdir("Data/Images")]
images = [html.Img(src=image_path, style={"max-height": "300px"}) for image_path in image_paths]
game_names = [game[:-4] for game in os.listdir("Data/Images")]

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="GameRec"),
    html.Div(children=[
        html.Div(children="Game:", style={"margin-right": 15}),
        dcc.Dropdown(options=[{"label": game, "value": game} for game in game_names], style={"width": "100%"}),
    ], style={"display": "flex", "align-items": "center", "align-content": "stretch", "justify-content": "stretch"}),
    html.Div(children=images, style={"display": "flex", "flex-wrap": "wrap"})
])

if __name__ == '__main__':
    app.run_server(debug=True)
