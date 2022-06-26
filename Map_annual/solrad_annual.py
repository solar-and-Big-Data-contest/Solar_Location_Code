import plotly.express as px
import pandas as pd
import time
from tqdm import tqdm

df1 = pd.read_csv('Nrel_alldata.csv',encoding='cp949')
df1.rename(columns={'solrad_annual':'solrad_annual(kWh/m2/day)'},inplace=True)
px.set_mapbox_access_token(open("mapbox_token.py").read()) # you will need your own token

fig = px.scatter_mapbox(df1, lat="lat", lon="lng", color='solrad_annual(kWh/m2/day)',hover_name="주소",hover_data=["solrad_annual(kWh/m2/day)","노선명"],
                        color_continuous_scale=px.colors.cyclical.IceFire,zoom=7
                       )

fig.update_layout(mapbox={'style':'dark','zoom':7},showlegend=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
