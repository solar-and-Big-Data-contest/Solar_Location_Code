import pandas as pd
import plotly.express as px

df = pd.read_csv('location.csv')

fig = px.density_mapbox(df, lat='lat', lon='lng', radius=3,
                        center=dict(lat=37.559819, lon=126.963895), zoom=5,
                        )
fig.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "source": [
                "http://api.vworld.kr/req/wmts/1.0.0/5442922B-39B0-355B-B773-7113F506F982/Satellite/{z}/{y}/{x}.jpeg"
            ]
            
        },
        {
            "sourcetype": "raster",
            "source": [
                "http://api.vworld.kr/req/wmts/1.0.0/5442922B-39B0-355B-B773-7113F506F982/Hybrid/{z}/{y}/{x}.png"
            ]

        }
      ])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

