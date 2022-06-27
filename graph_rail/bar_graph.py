import os, os.path, json, folium, requests, re
from folium import plugins
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from folium.plugins import MarkerCluster
import requests; from urllib.parse import urlparse
import pandas as pd

Area_Data = pd.read_csv('train_area.csv')
Rail_Data = pd.read_csv('nrel_allData.csv',encoding='cp949')

Mon = ['노선명','1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월']
Rail_D = Rail_Data.loc[:,['ac_annual','노선명']]
Rail_D = Rail_D.groupby('노선명').sum().astype(int)
Rail_D = Rail_D.sort_values(by='ac_annual',ascending=False)

Area_Data = Area_Data.sort_values(by='면적',ascending=False)

x1 = list(Area_Data.iloc[0:7,1])
y1 = list(Area_Data.iloc[0:7,2])

x2 = list(Rail_D.index)
x2 = x2[:7]
y2 = list(Rail_D.iloc[0:7,0] / 100)

x2[1],x2[2] = x2[2],x2[1]
x2[6],x2[5] = x2[5],x2[6]

plt.figure(figsize=(22,10))
plt.bar([i * 2 for i in range(len(x2))], y2, label='연간 예측 전력 발전량')
plt.bar([i * 2 + 0.8 for i in range(len(x2))], y1, label='면적')
plt.xticks([i * 2 + 0.25 for i in range(len(x2))], x2)

plt.title('연간 예측 전력 발전량 및 면적 추세')
plt.legend(['연간 예측 전력 발전량','면적'])
plt.show()
