from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import time
import pandas as pd
import sqlite3
import numpy as np
from statistics import mean

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import plotly.plotly as py
from flask import Flask, request, redirect, render_template, session, abort, url_for, json, make_response
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
import pygal

# plotly.tools.set_credentials_file(username='mtfaye', api_key='N9PkbhoY5zxhbU3LKqtb'

# API ACCESS

# Get the username from terminal
username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)


# Create our Spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token)


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True
app.title = 'hit-dash'
app.colors = {'background': '#5F5958'}


# Boostrap CSS
app.css.append_css({'external_url': 'https://codepen.io/mtfaye/pen/MWgpoyp.css'})

# Layouts
layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)
layout_table['font-size'] = '12'
layout_table['margin-top'] = '20'

layout_gauge = {
  "title": "Popularity",
  "width": 500,
  "xaxis": {
    "range": [-1, 1],
    "showgrid": False,
    "zeroline": False,
    "showticklabels": False
  },
  "yaxis": {
    "range": [-1, 1],
    "showgrid": False,
    "zeroline": False,
    "showticklabels": False
  },
  "height": 500,
  "shapes": [
    {
      "line": {"color": "850000"},
      "path": "M -.0 -0.025 L .0 0.025 L -1.0 1.22464679915e-16 Z",
      "type": "path",
      "fillcolor": "850000"
    }
  ]
}

# Gauge Chart
trace1 = {
  "name": "Popularity",
  "text": 2468,
  "type": "scatter",
  "x": [0],
  "y": [0],
  "marker": {
    "size": 28,
    "color": "850000"
  },
  "hoverinfo": "text+name",
  "showlegend": True
}
trace2 = {
  "hole": 0.5,
  "type": "pie",
  "marker": {"colors": ["rgba(44, 130, 201, 1)",
                        "rgba(52, 152, 219, 1)",
                        "rgba(34, 167, 240, 1)"]
             },
  "rotation": 90,
  "textinfo": "text",
  "hoverinfo": "label",
  "labels": ["61-100", "31-60", "0-30", ""],
  "values": [16, 16, 16, 50],
  "showlegend": True,
  "textposition": "inside"
}

data = [trace1, trace2]

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H1(children='hit-dash',
                                style={'color': 'white', 'fontSize':23, 'text-indent':10,'line-height': 50},
                                className='banner'
                                ),

                        html.Div(children='''
                                             Plot your artist
                                             ''',
                                 className='nine columns'
                                 )
                    ], className="row"
                ),
            html.Div([
                html.Div([

                        dcc.Input(id='input', value='', type='text',
                                  style={'display': 'inline-block', 'width': '30%'},
                                  placeholder=' Enter artist name'
                                  ),
                        html.Div(id='output_div'
                                 )
                    ], className="row"
                ),
                html.Div([
                    html.P('Choose features'),
                    dcc.Dropdown(
                        id='dropdown',
                        options=[{'label': 'Acousticness', 'value': 'ACO'},
                                 {'label': 'Energy', 'value': 'ENE'},
                                 {'label': 'Tempo', 'value': 'TEM'}],
                        value=[],
                        multi=True
                    )],className='row'),
                html.Div(
                    [
                        dcc.Graph(
                            id='feat-graph'
                        )
                    ],className='twelve columns'
                ),

                html.Div(
                    [
                        dash_table.DataTable(
                            id='table',
                            columns=[]
                        )

                    ], className="six columns"


                )
            ],className='row')
                ,
                html.Div(
                    [
                        html.P('Developed by Mouhameth T. Faye '
                               'and powered by Spotify Web API- ',
                               style={'display': 'inline'}
                               ),
                        html.A('mtfaye25@gmail.com',
                               href='mailto:mtfaye25@gmail.com'
                               )
                    ],className="twelve columns",
                    style={'fontSize': 10, 'padding-top': 18}
                )
            ], className="row"
        )
    ], className='ten columns offset-by-one'
)



@app.callback(Output('output_div','children'),
              [Input('input', 'value')])

def update_fig(input_data):
    # Get list of tracks for a given artist
    results = spotifyObject.search(input_data,limit=30)
    print(json.dumps(results, indent=4))

    # Get the list of tracks name
    tids = []
    for i, t in enumerate(results['tracks']['items']):
        # print(' ', i, t['name'])
        tids.append(t['uri'])


    # Create DataFrame for results
    df_results = pd.DataFrame(results['tracks']['items'])

    # Get features
    features = spotifyObject.audio_features(tids)

    # for feature in features:
    #     print(json.dumps(feature, indent=4))
    #  Create DataFrame for features
    df_features = pd.DataFrame(features)


    # Lets concat df_results and df_features
    df_results.reset_index(drop=True, inplace=True)
    df_features.reset_index(drop=True, inplace=True)
    global df


    df = pd.concat([df_results, df_features], axis=1)
    df = df.loc[:, ~df.columns.duplicated()]

    # Drop unnecessary columns
    df = df.drop([
        'available_markets', 'album', 'explicit', 'artists', 'disc_number', 'href', 'is_local', 'uri',
        'preview_url', 'type', 'external_ids', 'external_urls', 'id', 'track_href'
    ], axis=1)

    print(df.dtypes)

    connex = sqlite3.connect('spotify-data.db')
    # cur = connex.cursor()

    df.to_sql(name='Audio',
              con=connex,
              if_exists='replace'
              )

    con = sqlite3.connect('spotify-data.db')
    df = pd.read_sql_query('SELECT * FROM Audio', con)


    return[
        html.Div([
            html.H5(
                u"{}".format(input_data),
                style={'fontSize': 20, 'font-weight':'bold', 'text-indent':10, 'text-align':'center'}
            )
        ], className='twelve columns'),
          html.Div([
              html.Div(

                  [html.P('List of analysed tracks'),
                      html.Div(
                          html.Table(
                              [html.Tr([
                                  html.Th()
                              ])] +
                              # Body
                              [
                                  html.Tr(
                                      [
                                          html.Td(
                                              html.A(
                                                  df.iloc[i]['name'],
                                                  href=df.iloc[i]["name"],
                                                  target="_blank"
                                              )
                                          )
                                      ]
                                  )
                                  for i in range(len(df.name))
                              ]
                          ), style={"height": "350px", "width": "100", 'float': 'right', "overflowY": "scroll"}

                      )

                  ], className='four columns'),

                      html.Div([
                          html.Div([
                              daq.Gauge(
                                  id='popularity-graph',
                                  label='Popularity',
                                  color={"gradient": True,
                                         "ranges": {"lightblue": [0, 60], "blue": [60, 80], "darkblue": [80, 100]}},
                                  value=mean(list(df.popularity)),
                                  max=100,
                                  min=0,
                                  size=200
                              )
                          ], className='nine columns'),
                          html.Div([
                              daq.Gauge(
                                  id='danceability',
                                  label='Danceability',
                                  color={"gradient": True,
                                         "ranges": {"lightblue": [0, 0.6], "blue": [0.6, 0.8], "darkblue": [0.8, 1]}},
                                  value=mean(list(df.danceability)),
                                  max=1,
                                  min=0,
                                  size=100
                              )
                          ], className='three columns')

                      ],className='six columns')

          ],className='twelve columns')

    ]

@app.callback(Output('feat-graph','figure'),
              [Input('dropdown','value')])
def update_graph(selector):
    data = [{'y': df['acousticness'], 'type': 'scatter', 'name': 'Acousticness', 'mode':'lines',
                              'color':'firebrick'},
            {'y': df['instrumentalness'], 'type': 'scatter', 'name': 'Instrumentalness', 'mode':'lines+markers',
                              'color': 'firebrick'},
            {'y': df['energy'], 'type': 'scatter', 'name': 'Energy', 'mode':'markers',
                              'color': 'firebrick'}
                             ]
    for item in selector:
        for i in item:
            data.append(item[i])

        figure={'data': data,
                'layout': {
                       'title': 'Tracks features'
                    }
                }
        return figure






if __name__ == '__main__':
    app.run_server(debug=True, port=8050)



