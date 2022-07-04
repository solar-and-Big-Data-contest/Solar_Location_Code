# 설치 비용 계산해보기
'''
100kw 생산하는데 180000000원(1억 8천만)
http://www.agrinet.co.kr/news/articleView.html?idxno=162229

1kw 생산하는데 약 8~15m^2이 필요하다. 여기서 13m^2당 설비용량 1kw로 계산한다.
https://recloud.energy.or.kr/service/regi_require.do(재생에너지 클라우드플랫폼)
따라서 각각의 노선의 면적을 이용해 설비용량을 계산한다. 
설비용량 만큼 설치했을때 연 생상되는 전력량이 nrel에 나온값이다(내 생각).
우리가 구하는 값은 여기서 설비용량을 구한후 설치하는 비용을 구하면 된다

수식
설비용량 = 노선의 면적 / 13
설치비용 = (설비용량 / 100kw) * 180000000
여기서 (설비용량 / 100kw)는 그 지역에서 100kw 생산하기 위해 설치하는 
'''
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

    
Rail_Data = pd.read_csv('nrel_allData.csv',encoding='cp949')  # nrel 데이터를 불러온다.

Mon = ['노선명','1월','2월','3월','4월','5월','6월','7월','8월','9월','10월','11월','12월']  # x축 Data preprocessing
Rail_D = Rail_Data.loc[:,['ac_annual','노선명','면적']]       # 원하는 data만 가져온다. 연간 예측 발전량, 노선명, 면적
Rail_D = Rail_D.groupby('노선명').sum().astype(int)          # 노선명끼리 묶은 후 면적과 연간 예측 발전량을 합쳐준다.
Rail_D = Rail_D.sort_values(by='ac_annual',ascending=False)    # 연간 예측 발전량을 기준으로 내림차순으로 정렬해준다.

installed_capacity = list(Rail_D['면적'].apply(lambda x: x / 13))  
# 설비용량 = 노선의 면적 / 13
Rail_D['설비용량'] = installed_capacity      # 새로운 col을 만들어 설비용량,설치비용을 넣어준다.


install_cost = list(Rail_D['설비용량'].apply(lambda x: (x / 100) * 180000000))
# 설치비용 = (설비용량 / 100kw) * 180000000
Rail_D['설치비용'] = install_cost

Rail_D = Rail_D.astype(int)                # 정수형태로 바꿔준다.

y = Rail_D.iloc[:7,3]     # y축은 설치 비용
x = list(Rail_D.index)    # x축은 상위 7개 노선명
x = x[:7]



plt.figure(figsize=(20,10))    

colors = sns.color_palette('summer', len(x)) ## 바 차트 색상
 
xtick_label_position = list(range(len(x))) ## x축 눈금 라벨이 표시될 x좌표
plt.xticks(xtick_label_position, x) ## x축 눈금 라벨 출력
 
plt.bar(xtick_label_position, y, color=colors) ## 바차트 출력
plt.plot(xtick_label_position, y, color='g',
         linestyle='--', marker='o') ## 선 그래프 출력
plt.title('설치비용', fontsize=20)
plt.show()
