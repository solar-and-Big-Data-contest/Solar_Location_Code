import plotly.express as px
import pandas as pd
import time
from tqdm import tqdm

df2 = pd.read_csv('Nrel_alldata.csv',encoding='cp949')

px.set_mapbox_access_token(open("mapbox_token.py").read()) # you will need your own token



fig = px.scatter_mapbox(df2, lat="lat", lon="lng", color='ac_annual',hover_name="주소",hover_data=["ac_annual"],
                        color_continuous_scale=px.colors.sequential.Viridis,zoom=7
                       )

fig.update_layout(mapbox={'style':'dark','zoom':7},showlegend=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

