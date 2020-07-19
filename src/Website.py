import dash
import os

import dash_core_components as dcc
import dash_html_components as html

github_path = "https://raw.githubusercontent.com/KamWithK/GameRec/11208ae2c94d5b22dc0d5a4fc00fcd38f8d9255a/Data/Images/"
image_paths = [github_path + image for image in os.listdir("Data/Images")]
images = [html.Img(src=image_path) for image_path in image_paths]

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children="GameRec"),
    *images
])

if __name__ == '__main__':
    app.run_server(debug=True)
