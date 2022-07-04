# 경전선 구간별 태양 입사량 표

import os, os.path, json, folium, requests, re
from folium import plugins
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from folium.plugins import MarkerCluster
import requests; from urllib.parse import urlparse
import pandas as pd


Solarad_df = pd.read_csv('nrel_alldata.csv',encoding='cp949')
Solrad = list()     #  연간 태양광 입사량을 담을 빈 리스트
Rail = list()       # 노선명을 담을 빈 리스트


for i in range(len(Solarad_df)):    # 경전선, 경전선 추가의 노선값만 가져온다
    if Solarad_df.loc[i,'노선명'] == '경전선' or Solarad_df.loc[i,'노선명'] == '경전선 추가':      
        Rail.append(Solarad_df.loc[i,'노선명']),Solrad.append(Solarad_df.loc[i,'solrad_annual'])

        
        
Rail = Rail[::-1]    # rail, solrad갑을 뒤집어 준다.
Solrad = Solrad[::-1]
Rail_df = pd.DataFrame({'노선명':Rail,'solrad_annaul':Solrad})    # 새로운 dataFrame을 만든다.

y = list(Rail_df.loc[:,'solrad_annaul'])
x = [i for i in range(4209)]

plt.figure(figsize=(20,10))
plt.ylim(4.4,5.5)
plt.title('경전선의 구간별 연간 태양 입사량')
plt.bar(x,y)

plt.show()
