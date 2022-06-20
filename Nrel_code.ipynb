import os, os.path, requests, json
import folium
from folium.plugins import MarkerCluster
import requests; from urllib.parse import urlparse
import pandas as pd

Mon = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
API_KEY = "cpek8MOm9nrLsjNg6l3l8Ga7gsKMjTfwQWD69cif"
# Data = pd.read_csv('filename.csv',encoding = 'cp949') # csv 파일일 경우 사용
Data = pd.read_excel('유휴부지목록 (22.03월).xlsx',engine = "openpyxl")        # excel 파일일 경우 사용

def calNreldata_monthly(system_capacity = 4, azimuth = 180, tilt = 20,lat = 40,lng = -105):
   
    result = {}
    system_capacity = system_capacity * 0.15
    URL_PVWATTS6 =  f"https://developer.nrel.gov/api/pvwatts/v6.json?api_key=cpek8MOm9nrLsjNg6l3l8Ga7gsKMjTfwQWD69cif" + "&lat="+str(lat)+"&lon="+str(lng)+"&system_capacity="+ str(system_capacity)+"&azimuth=180&tilt=40&array_type=1&module_type=1&losses=10"

    response = requests.get(URL_PVWATTS6)
    json_obj = response.json()

    ac_annual = json_obj['outputs']['ac_annual']
    solrad_mon = list(json_obj['outputs']['solrad_monthly'])
    ac_Mon = list(json_obj['outputs']['ac_monthly'])
    solrad_annual = json_obj['outputs']['solrad_annual']


    AllData = pd.DataFrame({'ac_Mon' : ac_Mon,'solrad_mon' : solrad_mon},index=Mon,)
    
    return AllData,ac_annual,solrad_annual


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
'''
148번째 데이터 서울시 서초구 서초동 산36가 경도,위도값이 안되어 
서울시 서초구 서초동 산36-2로 바꿈.
'''
if __name__ == '__main__':
    cnt = len(Data.iloc[:,3])
    print("총 갯수: ", cnt)
    for i in range(1,cnt):         #엑셀파일은 행 이름부터 0번지를 사용한다.
        print(i,"번째 주소")
        area = Data.iloc[i,3]   #i번째 행, 3번째 열(면적)
        loa = Data.iloc[i,1]
        All_name.append(loa)
        print("면적",area)
        L = get_location(loa)
        print(loa)   #i번째 행, 1번째 열(주소)
        lat, lng = L['lat'], L['lng']
        print(lat,lng)
        
        All_lat.append(lat)
        All_lng.append(lng)
    
        result = calNreldata_monthly(area, lat, lng)
        print(result[0])
        print('ac_annual:',result[1])
        print('solrad_annual: ',result[2])
        
        print()
        print()
        
        
Data.loc[:,'lat'] = All_lat
Data.loc[:,'lng'] = All_lng
Data.loc[:, 'name'] = All_name
All_Data = Data.iloc[:,[1,6,7]]

m = folium.Map(
    tiles='Stamen Toner',
    zoom_start=15
)
temp = Data[['lat','lng','name']]

marker_cluster = MarkerCluster().add_to(m)

for lat,lng,name in zip(temp['lat'],temp['lng'],temp['name']):
    if lat == 0 and lng == 0: continue
    folium.Marker([lat,lng],icon=folium.Icon(color='green'),tooltip = name).add_to(marker_cluster)
    
m
