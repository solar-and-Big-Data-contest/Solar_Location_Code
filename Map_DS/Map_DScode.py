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

df_installation = pd.read_csv('20220623_태양광+발전소+누적+실치현황.csv')
df_power_generation = pd.read_csv('20220623_2021년+신규+발전량+현황.csv')
df_installation = df_installation.iloc[:,[0,5]]   # 필요한 값만 가져온다(시도별 이름, 태양전지 개수)

df_installation.rename(columns={'구분':'name'},inplace=True)
df_installation.rename(columns={'누적 발전소 개소(2021년까지)': '태양 전지 개수'},inplace=True) 

for idx,dic in enumerate(Map_geo['features']):
    dic['properties'].update({'name':str(df_installation.iloc[idx,0]),'태양 전지 개수':str(df_installation.iloc[idx,1]),'html':str(0)})
    txt = f'<b><h4>{df_installation.iloc[idx,0]}</h4></b>태양전지 설치 개수: {str(df_installation .iloc[idx,1])}'   # html로 작성하여 딕셔너리에 넣는다.
    dic['properties']['html'] = txt   
    

    
m = folium.Map(
    location=[37.559819, 126.963895],     # 서울의 위도,경도를 중심으로 잡는다.
    tiles='OpenStreetMap',
    zoom_start=7, 
)

cho = folium.Choropleth(
    geo_data=Map_geo,
    data=df_installation,
    fill_color='OrRd',
    columns=['name','태양 전지 개수'],
    key_on = 'feature.properties.name',
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name='태양 전지 개수'
).add_to(m)

plugins.Fullscreen(position='topright',
                   title='click to expand',
                   title_cancel='Click to Exit',
                   force_separate_button=True
                  ).add_to(m)

cho.geojson.add_child(folium.features.GeoJsonTooltip(['html'],labels=False))
title_html = '<h3 align="center" style="font-size:20px"><b>solar</b></h3>'
m.get_root().html.add_child(folium.Element(title_html))
folium.LayerControl().add_to(m)
m
