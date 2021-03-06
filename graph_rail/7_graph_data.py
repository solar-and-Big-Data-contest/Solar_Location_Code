# 상위 7개 그래프 표현

import os, os.path, json, folium, requests, re
import numpy 
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
    
df = pd.read_csv('nrel_allData.csv',encoding='cp949')
Mon = ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월','노선명']
df_ac_mon = df.iloc[:,1:13]
df_ac_mon['노선명'] = df.loc[:,'노선명']
df_ac_mon.columns = Mon

df_ac_mon = df_ac_mon.groupby('노선명').sum().astype(int)     # 노선명을 기준으로 월간 예측 전력 발전량을 합친다.


x = list(df_ac_mon.columns)
plt.figure(figsize=(15,5))

color = ['purple','mediumorchid','magenta','blueviolet','blueviolet','darkslateblue','mediumblue']
Rail_name = ['경전선','중앙선','동해중부 미건설선','장항선','경부선','경춘선','전라선']

for i in range(len(Rail_name)):
    y = list(df_ac_mon.loc[Rail_name[i]])
    plt.plot(x,y,'o-',color = color[i])

plt.xlabel('월')
plt.title('예측 전력 발전량')

plt.rc('font', size=20)        # 기본 폰트 크기
plt.rc('axes', labelsize=20)   # x,y축 label 폰트 크기
plt.rc('xtick', labelsize=20)  # x축 눈금 폰트 크기 
plt.rc('ytick', labelsize=14)  # y축 눈금 폰트 크기
plt.rc('legend', fontsize=20)  # 범례 폰트 크기

plt.legend(Rail_name,loc='upper center', ncol=2, bbox_to_anchor=(-0.4, 1))

plt.show()
