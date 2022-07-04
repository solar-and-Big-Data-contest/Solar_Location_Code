# 시군별 전력사용량 지도 표현

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
    
Map_geo = json.load(open('TL_SCCO_CTPRVN.json',encoding='utf-8')) # json geo 파일 불러들이기
City_df = pd.read_csv('시군별 전력사용량.csv',encoding='cp949')
City_df.drop(columns='Unnamed: 0',axis=0,inplace=True)

All_sum = list()
for i in range(len(City_df)):       # 12개월을 모두 합친 연간 총 전력사용량 구하기
    Sum = 0
    for j in range(4,16):
        if '-' in City_df.iloc[i,j]: continue
        Sum += int(re.sub(",","",City_df.iloc[i,j]))
    
    All_sum.append(Sum)
    
City_df['연간 총 전력사용량'] = All_sum   # 연간 총 전력사용량을 담을 col 생성
City_df = City_df.loc[:,['시도','연간 총 전력사용량']].groupby('시도').sum()   # 같은 시도끼리 모두 묶어 더한다.
Name_index = City_df.index
City_df['시도'] = Name_index

All_name = list()
All_Sum = list()

for idx,dic in enumerate(Map_geo['features']):          # geojson파일 순서가 같도록 전처리
    All_name.append(dic['properties']['CTP_KOR_NM'])
    if dic['properties']['CTP_KOR_NM'] in Name_index:  
        All_Sum.append(City_df.loc[dic['properties']['CTP_KOR_NM'],'연간 총 전력사용량'])
    else: 
        All_Sum.append(0)
        
Sort_df = pd.DataFrame({'시도':All_name, '연간 총 전력사용량': All_Sum})  # 필요한값만 가져와 새로운 dataframe 생성

for idx,dic in enumerate(Map_geo['features']):
    dic['properties'].update({'html':str(0)})
    txt = f'<b><h4>{Sort_df.iloc[idx,0]}</h4></b>연간 총 전력사용량: {str(Sort_df.iloc[idx,1])}'   # html로 작성하여 딕셔너리에 넣는다.
    dic['properties']['html'] = txt   

m = folium.Map(
    location=[37.559819, 126.963895],     # 서울의 위도,경도를 중심으로 잡는다.
    tiles='OpenStreetMap',
    zoom_start=7, 
)

cho = folium.Choropleth(
    geo_data=Map_geo,
    data=Sort_df,
    fill_color='OrRd',
    columns=['시도','연간 총 전력사용량'],
    key_on = 'feature.properties.CTP_KOR_NM',
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name='연간 총 전력사용량'
).add_to(m)

cho.geojson.add_child(folium.features.GeoJsonTooltip(['html'],labels=False))
title_html = '<h3 align="center" style="font-size:20px"><b>연간 총 전력사용량</b></h3>'
m.get_root().html.add_child(folium.Element(title_html))

m
