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

df = pd.read_csv("국가철도공단_철도유휴부지DB_20210902.csv",encoding='cp949')
df_Location = pd.read_csv('location.csv')


def calNreldata_monthly(system_capacity = 4, azimuth = 180, tilt = 20,lat = 40,lng = -105):   #nrel 사용
    system_capacity = system_capacity * 0.15
    URL_PVWATTS6 =  f"https://developer.nrel.gov/api/pvwatts/v6.json?api_key=4QsgChvEXKX1cnKcKGieUfayxaRA3q2pBT9K5I4x" + "&lat="+str(lat)+"&lon="+str(lng)+"&system_capacity="+ str(system_capacity)+"&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10"

    response = requests.get(URL_PVWATTS6)
    json_obj = response.json()
    print(json_obj)
    try: 
      ac_annual = json_obj['outputs']['ac_annual']
      solrad_mon = list(json_obj['outputs']['solrad_monthly'])
      ac_Mon = list(json_obj['outputs']['ac_monthly'])
      solrad_annual = json_obj['outputs']['solrad_annual']
      
      return ac_annual,solrad_mon,ac_Mon,solrad_annual

    except : return ['0', '0', '0', '0']


df = df.iloc[:,[1,2,3]]        # 필요한 값만 가져온다.
df['lat'] = df_Location.iloc[:,1]    
df['lng'] = df_Location.iloc[:,2]
Location = list()        # 주소를 담을 변수

if __name__ == '__main__':
    Len = len(df.iloc[:,1])
    for i in range(Len):        # 모든 데이터를 다 돌면서 nrel에 넣는다.
        print(i,"번쨰")
        area = df.loc[i,' 면적(공부) ']  #면적 받아오기
        lat = df.loc[i,'lat']   # 위도
        lng = df.iloc[i,'lng']   # 경도
        
        ac_annual,solrad_mon,ac_Mon,solrad_annual = calNreldata_monthly(area,180,40,lat,lng)

        if ac_annual == '0' and solrad_mon == '0' and ac_Mon == '0' and solrad_annual == '0': continue    
        # 만약 위경도가 잘못됐다면 continue한다.
        Location.append(df.iloc[i,0])
        if i==19450:
          # 처음 반복문을 돌 때 데이터프레임 생성
          Land_df2=pd.DataFrame([ac_Mon+solrad_mon],columns=['ac_monthly_1','ac_monthly_2','ac_monthly_3','ac_monthly_4','ac_monthly_5','ac_monthly_6','ac_monthly_7','ac_monthly_8','ac_monthly_9','ac_monthly_10','ac_monthly_11','ac_monthly_12','solared_mon_1','solared_mon_2',
                                       'solared_mon_3','solared_mon_4','solared_mon_5','solared_mon_6','solared_mon_7','solared_mon_8','solared_mon_9','solared_mon_10','solared_mon_11','solared_mon_12'])
          Land_df2['solrad_annual']=solrad_annual
          Land_df2['ac_annual']=ac_annual

        else:
            Land_df2.loc[i]=ac_Mon+solrad_mon+[solrad_annual]+[ac_annual]
        print()
        print()
        
Land_df2['주소'] = Location
Land_df2
