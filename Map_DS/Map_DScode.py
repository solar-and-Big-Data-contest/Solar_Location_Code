

import os, os.path, json, folium, requests
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

df = pd.read_csv('20220623_태양광+발전소+누적+실치현황.csv')

df = df.iloc[:,[0,5]]   # 필요한 값만 가져온다(시도별 이름, 태양전지 개수)

Solar_Data = df.iloc[:,1].astype(str)       # 각 값들을 문자로 바꾼다
df.rename(columns={'구분':'name'},inplace=True)   # 컬럼들의 이름을 바꾼디.
df.rename(columns={'누적 발전소 개소(2021년까지)':'name'},inplace=True)

for idx,dic in enumerate(Map_geo['features']):
    dic['properties'].update({'name':str(0),'cnt':str(df.iloc[idx,1])}) # 모든 데이터를 다 돌면서 geojson파일에 시도별 이름과 태양전기 개수를 추가시킨다.
    txt = f'<b><h4>{df.iloc[idx,0]}</h4></b>태양전지 설치 개수: {str(df.iloc[idx,1])}'   # html로 작성하여 딕셔너리에 넣는다.
    dic['properties']['name'] = txt   

m = folium.Map(
    location=[37.559819, 126.963895],     # 서울의 위도,경도를 중심으로 잡는다.
    tiles="OpenStreetMap",
    zoom_start=7, 
)


cho = folium.Choropleth(        # 경계선 그리기
    geo_data=Map_geo,
    data=Solar_Data,
    name='태양전지 현황',
    columns=[df.iloc[:,0],Solar_Data],
    fill_color='RdYlGn',
    fill_opacity=0.7,
#     key_on = 'features.properties.name',
    line_opacity=0.5,
    legend_name='soloar'
).add_to(m)

plugins.Fullscreen(position='topright',
                   title='click to expand',
                   title_cancel='Click to Exit',
                   force_separate_button=True
                  ).add_to(m)

cho.geojson.add_child(folium.features.GeoJsonTooltip(['name'],labels=False))    # 지도에 마우스를 올렸을때 정보 
title_html = '<h3 align="center" style="font-size:20px"><b>solar</b></h3>'
m.get_root().html.add_child(folium.Element(title_html))
folium.LayerControl().add_to(m)
m
