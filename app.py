from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import os
import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import pandas as pd
import sqlite3
from statistics import mean

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
import plotly.graph_objs as go


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

                    dcc.Dropdown(
                        id='dropdown',
                        options=[{'label': 'Acousticness', 'value': 'Acousticness'},
                                 {'label': 'Liveness', 'value': 'Liveness'},
                                 {'label': 'Energy', 'value': 'Energy'},
                                 {'label': 'Valence', 'value': 'Valence'}
                                 ],
                        value='All',
                        multi=True,
                        placeholder='Choose a feature'
                    )],className='six columns'),
                html.Div(
                    [
                        dcc.Graph(
                            id='feat-graph'
                        )
                    ],className='nine columns'
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

def update_div(input_data):
    # Get list of tracks for a given artist
    results = spotifyObject.search(input_data,limit=30)
    # print(json.dumps(results, indent=4))

    # Get the list of tracks name
    tids = []
    for i, t in enumerate(results['tracks']['items']):
        # print(' ', i, t['name'])
        tids.append(t['uri'])


    # Create DataFrame for results
    df_results = pd.DataFrame(results['tracks']['items'])

    # Get features
    features = spotifyObject.audio_features(tids)

    for feature in features:
        print(json.dumps(feature, indent=4))
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

    # print(df.dtypes)

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

                      html.Div([html.P(html.H5(u"{}".format(input_data),
                                               style={'fontSize': 20, 'font-weight':'bold', 'text-indent':10,
                                                      'text-align':'center'}
            )),
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

    options_data={
        'Acousticness': df.acousticness,
        'Liveness': df.liveness,
        'Energy': df.energy,
        'Valence':df.valence,

    }

    data=[]
    for i in selector:
        data.append({
            'y': options_data[i], 'type': 'Scatter', 'mode': 'lines+markers'
            })

    figure= {
            'data': data,
            'layout':
                {
                    'title':'Tracks Features'

                }
        }
    return figure




if __name__ == '__main__':
    app.run_server(debug=True, port=8050)



