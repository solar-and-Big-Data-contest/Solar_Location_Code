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
    
df = pd.read_csv('Nrel_alldata.csv',encoding='cp949')
df2 = pd.read_csv('국가철도공단_철도유휴부지DB_20210902.csv',encoding='cp949')
Mon = ['1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월','주소']
df_ac_mon = df.iloc[:,1:13]
df_ac_mon['주소'] = df.iloc[:,27]
df_ac_mon.columns = Mon

for i in range(len(df_ac_mon)):
    temp = df_ac_mon.loc[i,'주소']
    Str = '-1'
    if '경기' in temp:  Str = '경기도'
    elif '강원' in temp: Str = '강원도'
    elif '충청북' in temp: Str = '충청북도'    
    elif '충청남' in temp: Str = '충청남도'    
    elif '전라북' in temp: Str = '전라북도'    
    elif '전라남' in temp: Str = '전라남도'    
    elif '경상북' in temp: Str = '경상북도'    
    elif '경상남' in temp: Str = '경상남도'      
    elif '세종' in temp: Str = '세종특별자치시'    
    elif '대전' in temp: Str = '대전광역시'    
    elif '울산' in temp: Str = '울산광역시'    
    elif '광주' in temp: Str = '광주광역시'    
    elif '인천' in temp: Str = '인천광역시'    
    elif '대구' in temp: Str = '대구광역시'    
    elif '부산' in temp: Str = '부산광역시'    
    elif '서울' in temp: Str = '서울특별시'

    if Str != '-1': df_ac_mon.loc[i,'주소'] = Str
    
df_ac_mon = df_ac_mon.groupby('주소').sum().astype(int)
x = list(df_ac_mon.columns)
plt.figure(figsize=(15,5))

name = df_ac_mon.index

color = ['black','bisque','forestgreen','slategrey','darkorange','royalblue','azure','gold','red','rosybrown','yellow','aqua','thistle','lawngreen','violet']
for i in range(len(df_ac_mon)):
    y = list(df_ac_mon.iloc[i])
    plt.plot(x,y, color = color[i])
    
plt.xlabel('월')
plt.title('예측 전력 발전량')

plt.rc('font', size=20)        # 기본 폰트 크기
plt.rc('axes', labelsize=20)   # x,y축 label 폰트 크기
plt.rc('xtick', labelsize=20)  # x축 눈금 폰트 크기 
plt.rc('ytick', labelsize=14)  # y축 눈금 폰트 크기
plt.rc('legend', fontsize=20)  # 범례 폰트 크기

plt.legend(name,loc='upper center', ncol=2, bbox_to_anchor=(-0.3, 1))
plt.show()

plt.show()
