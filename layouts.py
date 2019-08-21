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

#
# # my_raw_value = statistics.mean(list(df.popularity))
# #
# # # Rotate dial
# # h = 0.24
# # k = 0.5
# # r = 0.15
# # # Map my_raw_value to degrees. my_raw_value is between 0 and 300
# # theta = (100 - my_raw_value) * 180 / 100
# # # and then into radians
# # theta = theta * math.pi / 180
# # x = h + r*math.cos(theta)
# # y = k + r*math.sin(theta)
#
#
