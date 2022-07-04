# 25개 노선 모든 그래프
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
    
Mon = ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월','노선명']
df = pd.read_csv("nrel_alldata.csv",encoding='cp949')
df_ac_mon = df.iloc[:,1:13]
df_ac_mon['노선명'] = df.loc[:,'노선명']
df_ac_mon.columns = Mon

df_ac_mon = df_ac_mon.groupby('노선명').sum().astype(int)

All_sum = list()

for i in range(len(df_ac_mon)):     # 범례를 순서대로 하기 위해 총 발전량을 계산한다.
    Sum = 0
    for j in range(12):
        Sum += df_ac_mon.iloc[i,j]
    All_sum.append(Sum)
    

df_ac_mon['총 발전량'] = All_sum   # 총 발전량을 기준으로 정렬하고 총 발전량을 삭제한다.
df_ac_mon.sort_values(by='총 발전량',ascending=False,inplace=True)
df_ac_mon.drop(columns={'총 발전량'},inplace=True)        

x = list(df_ac_mon.columns)
plt.figure(figsize=(15,5))

name = df_ac_mon.index
color = ['purple','mediumorchid','magenta','blueviolet','blueviolet','darkslateblue','mediumblue','b','midnightblue','cornflowerblue','lightsteelblue','steelblue','aqua','darkslategray','turquoise'
         ,'aquamarine','springgreen','green','forestgreen','darkolivegreen','peru','chocolate','orangered','salmon','darkred']


for i in range(len(df_ac_mon)):
    y = list(df_ac_mon.loc[name[i]])
    plt.plot(x,y,'o-',color = color[i])


plt.title('예측 전력 발전량')

plt.rc('font', size=20)        # 기본 폰트 크기
plt.rc('axes', labelsize=20)   # x,y축 label 폰트 크기
plt.rc('xtick', labelsize=20)  # x축 눈금 폰트 크기 
plt.rc('ytick', labelsize=14)  # y축 눈금 폰트 크기
plt.rc('legend', fontsize=20)  # 범례 폰트 크기

plt.legend(name,loc='upper center', ncol=2,fontsize=12.5,bbox_to_anchor=(1.2, 1))
plt.show()
