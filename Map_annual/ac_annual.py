import plotly.express as px
import pandas as pd
import time
from tqdm import tqdm

df2 = pd.read_csv('Nrel_alldata.csv',encoding='cp949')
df2.rename(columns={"ac_annual":"연간 예측 전력발전량(kWh)"},inplace = True)
px.set_mapbox_access_token(open("mapbox_token.py").read()) # you will need your own token



fig = px.scatter_mapbox(df2, lat="lat", lon="lng", color='연간 예측 전력발전량(kWh)',hover_name="주소",hover_data=["연간 예측 전력발전량(kWh)"],
                        color_continuous_scale=px.colors.sequential.Viridis,zoom=7
                       )

fig.update_layout(mapbox={'style':'dark','zoom':7},showlegend=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

