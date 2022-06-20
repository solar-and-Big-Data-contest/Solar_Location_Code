import os, os.path, requests, json
import folium
import matplotlib.pyplot as plt
import seaborn as sns
from folium.plugins import MarkerCluster
import requests; from urllib.parse import urlparse
import pandas as pd



if os.name == 'posix':  plt.rc("font", family="AppleGothic")    #mac일경우
else:   plt.rc("font", family="Malgun Gothic")    #그외에 다른거일경우
                               
Mon = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
API_KEY = "cpek8MOm9nrLsjNg6l3l8Ga7gsKMjTfwQWD69cif"
# Data = pd.read_csv('국가철도공단_철도유휴부지DB_20210902.csv',encoding = 'cp949') # csv 파일일 경우 사용
Data = pd.read_excel('유휴부지목록 (22.03월).xlsx',engine = "openpyxl")        # excel 파일일 경우 사용

def calNreldata_monthly(system_capacity = 4, azimuth = 180, tilt = 20,lat = 40,lng = -105):
    system_capacity = system_capacity * 0.15
    URL_PVWATTS6 =  f"https://developer.nrel.gov/api/pvwatts/v6.json?api_key=cpek8MOm9nrLsjNg6l3l8Ga7gsKMjTfwQWD69cif" + "&lat="+str(lat)+"&lon="+str(lng)+"&system_capacity="+ str(system_capacity)+"&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10"

    response = requests.get(URL_PVWATTS6)
    json_obj = response.json()

    ac_annual = json_obj['outputs']['ac_annual']
    solrad_mon = list(json_obj['outputs']['solrad_monthly'])
    ac_Mon = list(json_obj['outputs']['ac_monthly'])
    solrad_annual = json_obj['outputs']['solrad_annual']
    
    # print('ac_annual',ac_annual)
    # print('solared_mon',solrad_mon)
    # print('ac_Mon',ac_Mon)
    # print('solrad_annual',solrad_annual)

    return ac_annual,solrad_mon,ac_Mon,solrad_annual


def get_location(address):
  url = 'https://dapi.kakao.com/v2/local/search/address.json?query=' + address
  # 'KaKaoAK '는 그대로 두시고 개인키만 지우고 입력해 주세요.
  headers = {"Authorization": "KakaoAK 847f4572b1920bfb90d7b7aadd91b4c4"}
  api_json = json.loads(str(requests.get(url,headers=headers).text))
  address = api_json['documents'][0]['address']
  crd = {"lat": str(address['y']), "lng": str(address['x'])} # 위도, 경도
  address_name = address['address_name']

  return crd

All_lat = [0 for _ in range(1)]
All_lng = [0 for _ in range(1)]
All_name = [0 for _ in range(1)]
All_area = [0 for _ in range(1)]
'''
148번째 데이터 서울시 서초구 서초동 산36가 경도,위도값이 안되어 
서울시 서초구 서초동 산36-2로 바꿈.
'''


if __name__ == '__main__':
 
    cnt = len(Data.iloc[:,3])

    for i in range(1,cnt):
        print(i,'번째 주소')
        area = Data.iloc[i,3]   #i번째 행, 3번째 열(면적)
        Location = Data.iloc[i,1]
        print(Location)   #i번째 행, 1번째 열(주소)
        L = get_location(Data.iloc[i,1])
        lat, lng = L['lat'], L['lng']
        All_lat.append(lat)
        All_lng.append(lng)
        All_area.append(area)
        All_name.append(Location)
        print('lat,lng',lat,lng)
        ac_annual,solrad_mon,ac_Mon,solrad_annual = calNreldata_monthly(area,180,40,lat, lng)
        if i==1:
          # 처음 반복문을 돌 때 데이터프레임 생성
          df2=pd.DataFrame([ac_Mon+solrad_mon],columns=['ac_monthly_1','ac_monthly_2','ac_monthly_3','ac_monthly_4','ac_monthly_5','ac_monthly_6','ac_monthly_7','ac_monthly_8','ac_monthly_9','ac_monthly_10','ac_monthly_11','ac_monthly_12','solared_mon_1','solared_mon_2',
                                       'solared_mon_3','solared_mon_4','solared_mon_5','solared_mon_6','solared_mon_7','solared_mon_8','solared_mon_9','solared_mon_10','solared_mon_11','solared_mon_12'])
          df2['solrad_annual']=solrad_annual
          df2['ac_annual']=ac_annual

        else:
            df2.loc[i]=ac_Mon+solrad_mon+[solrad_annual]+[ac_annual]
  
        print()
        print()
        
Data.loc[:,'lat'] = All_lat
Data.loc[:,'lng'] = All_lng
Data.loc[:, 'name'] = All_name
Data.loc[:,'area'] = All_area
All_Data = Data.iloc[:,[1,6,7]]

m = folium.Map(
    location=[37.541, 126.986],
#     tiles='Stamen Toner',
    zoom_start=11
)
temp = Data[['lat','lng','name','area']]

marker_cluster = MarkerCluster().add_to(m)

plt.figure(figsize=(12,30))
sns.countplot(y=temp['name'],order=temp['name'].value_counts().index)
plt.title('태양광전지 설치 개수')
plt.show()


for lat,lng,name,area in zip(temp['lat'],temp['lng'],temp['name'],temp['area']):
    if lat == 0 and lng == 0: continue
    folium.Circle(location=[lat, lng],radius=area,color="#eb9e34",fill_color="red",popup="Circle popup",tooltip="Circle tooltip").add_to(m)
    folium.Marker([lat,lng],icon=folium.Icon(color='red'),tooltip = name).add_to(marker_cluster)
    
