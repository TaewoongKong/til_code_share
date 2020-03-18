```python
# api 이용을 위한 세팅 코드

import pandas as pd

import json
import requests

```

### 카카오 검색 -> 서칭된 결과물의 정보 json으로 빼오기


- url 형식 : https://developers.kakao.com/docs/restapi/search/ + 키워드
- query : 검색어
- apikey : 내 키
- 파라미터들



| 키 | 설명 | 필수 | 타입 |
|:------:|:------:|:------:|:------:|
|query|검색을 원하는 질의어|O|String|
|sort|결과 문서 정렬 방식|X (accuracy)|accuracy (정확도순) or recency (최신순)|
|page|결과 페이지 번호|X(기본 1)|1-50 사이 Integer|
|size|한 페이지에 보여질 문서의 개수|X(기본 10)|1-50 사이 Integer|



```python
#https://developers.kakao.com/docs/restapi/search#웹문서-검색

url = "https://dapi.kakao.com/v2/local/search/keyword.json?query=" + query
apikey = "8c2c3094684998813842167d9664dc32"
query = "스파크플러스"
result = requests.get(url, params = {'query':query, 'page':2}, headers={'Authorization' : 'KakaoAK ' + apikey})

json_obj = result.json()
```


```python
json_obj['documents'][6]
```




    {'address_name': '서울 성동구 성수동2가 273-13',
     'category_group_code': '',
     'category_group_name': '',
     'category_name': '서비스,산업 > 기업',
     'distance': '',
     'id': '1638220574',
     'phone': '',
     'place_name': '아나로그아키펜',
     'place_url': 'http://place.map.kakao.com/1638220574',
     'road_address_name': '서울 성동구 연무장15길 11',
     'x': '127.059519028852',
     'y': '37.5426770073045'}



### 이를 바탕으로 df 로 자동 저장하는 코드 작성


```python


list = []
for document in json_obj['documents']:
    information = [document['place_name'], document['phone'], document['road_address_name'], document['y'], document['x']]
    list.append(information)
    
df = pd.DataFrame(list, columns = ['place_name', 'phone', 'road_address_name', 'latitude', 'longitude'])
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>place_name</th>
      <th>phone</th>
      <th>road_address_name</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>스파크플러스 성수점</td>
      <td>02-555-3477</td>
      <td>서울 성동구 연무장15길 11</td>
      <td>37.5426725962657</td>
      <td>127.059332321196</td>
    </tr>
  </tbody>
</table>
</div>



### 카카오 검색창에 주소를 직접 꽂아 넣는 경우


```python
# 카카오맵 주소 검색 API: https://developers.kakao.com/docs/restapi/local#주소-검색

address = "관악구 관천로 19길 88"
url = "https://dapi.kakao.com/v2/local/search/address.json?&query=" + address
result = requests.get(url, headers={"Authorization":'KakaoAK ' + apikey})
json_obj = result.json()

# json의 첫번째는 [address] 를 통해 구 주소가 나오며, 두 번째는 [address_road]를 통해 신 주소가 나온다
```


```python
json_obj
```




    {'documents': [{'address': {'address_name': '서울 관악구 신림동 495-26',
        'b_code': '1162010200',
        'h_code': '1162068500',
        'main_adderss_no': '',
        'main_address_no': '495',
        'mountain_yn': 'N',
        'region_1depth_name': '서울',
        'region_2depth_name': '관악구',
        'region_3depth_h_name': '신사동',
        'region_3depth_name': '신림동',
        'sub_adderss_no': '',
        'sub_address_no': '26',
        'x': '126.917063252091',
        'y': '37.4870068078388',
        'zip_code': ''},
       'address_name': '서울 관악구 관천로19길 88',
       'address_type': 'ROAD_ADDR',
       'road_address': {'address_name': '서울 관악구 관천로19길 88',
        'building_name': '한송빌',
        'main_building_no': '88',
        'region_1depth_name': '서울',
        'region_2depth_name': '관악구',
        'region_3depth_name': '신림동',
        'road_name': '관천로19길',
        'sub_building_no': '',
        'undergroun_yn': '',
        'underground_yn': 'N',
        'x': '126.917063252091',
        'y': '37.4870068078388',
        'zone_no': '08702'},
       'x': '126.917063252091',
       'y': '37.4870068078388'}],
     'meta': {'is_end': True, 'pageable_count': 1, 'total_count': 1}}




```python
list = []
for document in json_obj['documents']:
    information = [document['road_address']['building_name'], document['address_name'], document['y'], document['x']]
    list.append(information)
    
df = pd.DataFrame(list, columns = ['building_name', 'address_name', 'latitude', 'longitude'])
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>building_name</th>
      <th>address_name</th>
      <th>latitude</th>
      <th>longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>한송빌</td>
      <td>서울 관악구 관천로19길 88</td>
      <td>37.4870068078388</td>
      <td>126.917063252091</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
