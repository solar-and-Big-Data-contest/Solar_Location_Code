# 매출액 구하기

import os, os.path, json, folium, requests, re
from folium import plugins
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from folium.plugins import MarkerCluster
import requests; from urllib.parse import urlparse
import pandas as pd
import seaborn as sns

if os.name == 'posix':  
    plt.rc("font", family="AppleGothic")    #mac일경우
else: 
    plt.rc("font", family="Malgun Gothic")    #그외에 다른거일경우

weight, SMP, REC = 1, 132, 54981
    
df = pd.read_csv('nrel_allData.csv',encoding='cp949')
df_ac_annual = df.loc[:,['노선명','ac_annual']]   # 원하는 값만 가져오기
df_ac_annual = df_ac_annual.groupby('노선명').sum().astype(int)  # 노선명을 기준으로 연간 총 전력량을 합친다.

df_rv = df_ac_annual.apply(lambda power_generation : (power_generation * SMP) + (power_generation * REC * weight))
# 예측수익 = (발전량 * SMP) + (발전량 * REC * 가중치) 
df_rv.sort_values(by=['ac_annual'],ascending=False,inplace=True)
df_rv.rename(columns={'ac_annual':'예측수익'},inplace=True)

x1 = df_rv.index   # 상위 7개 노선명만 나타낸다.
x1 = list(x1[0:7])
y1 = list(df_rv.iloc[:7,0])

plt.figure(figsize=(15,10))

colors = sns.color_palette('summer', len(x1)) ## 바 차트 색상
 
xtick_label_position = list(range(len(x1))) ## x축 눈금 라벨이 표시될 x좌표
plt.xticks(xtick_label_position, x1) ## x축 눈금 라벨 출력
 
plt.bar(xtick_label_position, y1, color=colors) ## 바차트 출력
plt.plot(xtick_label_position, y1, color='g',
         linestyle='--', marker='o') ## 선 그래프 출력
plt.title('예상 수익', fontsize=20)
plt.show()
