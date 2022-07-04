# 2021 신규 태양광 발전량 시각화

import os, os.path, json, folium, requests, re
from folium import plugins
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from folium.plugins import MarkerCluster
import requests; from urllib.parse import urlparse
import pandas as pd

if os.name == 'posix':  
    plt.rc("font", family="AppleGothic")    #mac일경우
else: 
    plt.rc("font", family="Malgun Gothic")    #그외에 다른거일경우

Map_geo = json.load(open('ctp_rvn.zip.geojson',encoding='utf-8')) # json geo 파일 불러들이기

df_power_generation = pd.read_csv('20220623_2021년+신규+발전량+현황.csv')

All_Sum = list() 
for i in range(len(df_power_generation)):    # 12개월을 모두 합친 연간 총 전력 발전량 구하기
    Sum = 0
    for j in range(1,13):
        Sum += float(re.sub(',','',df_power_generation.iloc[i,j]))
    All_Sum.append(int(Sum))
    
df_power_generation['2021 신규 태양광 발전량'] = All_Sum

for idx,dic in enumerate(Map_geo['features']):
    dic['properties'].update({'name':str(df_power_generation.iloc[idx,0]),'2021 신규 태양광 발전량':str(df_power_generation.iloc[idx,13]),'html':str(0)})
    txt = f'<b><h4>{df_power_generation.iloc[idx,0]}</h4></b> 2021 신규 태양광 발전량: {str(df_power_generation .iloc[idx,13])}'   # html로 작성하여 딕셔너리에 넣는다.
    dic['properties']['html'] = txt   



m = folium.Map(
    location=[37.559819, 126.963895],     # 서울의 위도,경도를 중심으로 잡는다.
    tiles='OpenStreetMap',
    zoom_start=7, 
)

cho = folium.Choropleth(
    geo_data=Map_geo,
    data=df_power_generation,
    fill_color='OrRd',
    columns=['구분','2021 신규 태양광 발전량'],
    key_on = 'feature.properties.name',
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name='2021 신규 태양광 발전량'
).add_to(m)

cho.geojson.add_child(folium.features.GeoJsonTooltip(['html'],labels=False))
title_html = '<h3 align="center" style="font-size:20px"><b>2021 신규 태양광 발전량</b></h3>'
m.get_root().html.add_child(folium.Element(title_html))

m
