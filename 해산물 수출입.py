#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# 화면에 출력하는 데이터 프레임의 최대 row 수를 500으로 설정합니다.
pd.set_option('display.max_rows', 500)

# 화면에 출력하는 데이터 프레임의 최대 column 수를 500으로 설정합니다.
pd.set_option('display.max_columns', 500)


# In[3]:


import matplotlib
import matplotlib.pyplot as plt  # 파이플롯 사용
import seaborn as sns
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')  # 한글코드를 더 선명하게 해주는 조치, 레티나 설정
matplotlib.rc('font', family='AppleGothic') # 폰트 설정
matplotlib.rc('axes', unicode_minus=False) # 마이너스 폰트가 깨지는 경우가 있으므로 조치


# In[4]:


df = pd.read_csv("해양수산부_국가별 수산물 수출입 현황 - 2019년 11월(월간).csv", encoding='euc-kr', engine='python')


# In[5]:


df = df.drop(['기준년월', '\t국가코드', '\tHSK품목코드', '\t수출입구분명','\t당월 누계 수출입중량','\t당월 누계 수출입미화금액', '\t데이터기준일자\t'], axis = 1)


# In[6]:


df_new_columns = []
for column in df.columns:
    df_new_columns.append(column.replace("\t", ""))
df.columns = df_new_columns


# In[7]:


# 전체 DF에 걸쳐있는 '' 제거
for column in df.columns:
    df[column] = df[column].str.replace("'", "")


# In[8]:


# object 타입으로 되어있는 숫자 데이터는 int처리
df['당월 수출입중량'] = df['당월 수출입중량'].astype(int)
df['당월수출입미화금액'] = df['당월수출입미화금액'].astype(int)


# In[9]:


df.columns = ['ex_im', 'nat', 'zone', 'item', 'item_weight','amount_dollar']


# In[10]:


df['item_price'] = pd.Series("%0.2f"%i for i in (df.amount_dollar) / (df.item_weight))


# In[11]:


df.loc[df['item_price'] == 'nan', 'item_price'] = 0
df.loc[df['item_price'] == 'inf', 'item_price'] = 0


# In[12]:


df.loc[df['zone'] == '', 'zone'] = '무소속'


# In[13]:


df['item'] = pd.Series(i.split('(')[0] for i in df['item'])


# In[14]:


df.loc[df['item'] == '기타어류', 'item'] = '기타'
df.loc[df['item'] == '냉동한 것', 'item'] = '기타'
df.loc[df['item'] == '어류조제/저장제품', 'item'] = '어류조제품'
df.loc[df['item'] == '천일염', 'item'] = '소금'
df.loc[df['item'] == '식염', 'item'] = '소금'
df.loc[df['item'] == '조제한식용해조류', 'item'] = '해조류'
df.loc[df['item'] == '해초류와 기타조류 기타', 'item'] = '해조류'
df.loc[df['item'] == '다랭이', 'item'] = '다랭이류'
df.loc[df['item'] == '오징어 기타', 'item'] = '오징어'
df.loc[df['item'] == '조미오징어', 'item'] = '오징어'
df.loc[df['item'] == '연체동물 기타', 'item'] = '기타'
df.loc[df['item'] == '기타어류의 기타', 'item'] = '기타'
df.loc[df['item'] == '수생무척추동물의 기타', 'item'] = '기타'
df.loc[df['item'] == '클램/ 새조개 및 피조개 기타', 'item'] = '조개'
df.loc[df['item'] == '캐비아 대용물', 'item'] = '캐비아'
df.loc[df['item'] == '멸치[엔그라울리스', 'item'] = '멸치'
df.loc[df['item'] == '갑각류 기타', 'item'] = '갑각류'
df.loc[df['item'] == '염장이나 염수장한 것', 'item'] = '기타'
df.loc[df['item'] == '눈다랑어', 'item'] = '다랭이류'
df.loc[df['item'] == '다랑어 기타', 'item'] = '다랭이류'
df.loc[df['item'].str.contains('다랑어'), 'item'] = '다랭이류'
df.loc[df['item'].str.contains('다랭이'), 'item'] = '다랭이류'
df.loc[df['item'].str.contains('진주'), 'item'] = '진주'

df.loc[df['item'] == '패각', 'item'] = '조개류'
df.loc[df['item'] == '다랑어 기타', 'item'] = '다랭이류'
df.loc[df['item'] == '어류의간유/분획물', 'item'] = '조분'
df.loc[df['item'] == '기타 게살', 'item'] = '기타'
df.loc[df['item'] == '기타[분 조분 펠리트 포함', 'item'] = '조분'
df.loc[df['item'] == '어류의 고운 가루ㆍ거친 가루와 펠릿', 'item'] = '기타'
df.loc[df['item'] == '기타 수생무척추동물의 기타', 'item'] = '기타'
df.loc[df['item'] == '붉은 대게살', 'item'] = '기타'
df.loc[df['item'] == '어류의액스', 'item'] = '기타'
df.loc[df['item'] == '기타 수생무척추동물의 기타', 'item'] = '기타'
df.loc[df['item'] == '기타[분ㆍ조분 및 펠리트를 포함', 'item'] = '조분'
df.loc[df['item'] == '그 밖의 새우류', 'item'] = '새우류'
df.loc[df['item'] == '넙치[레인하드티우스 히포글러소이데스/히포글러서스 히포글러서스/히포글러서스 스테노레피스)', 'item'] = '넙치'
df.loc[df['item'] == '기타 냉동연육 외 기타', 'item'] = '기타'
df.loc[df['item'] == '분한천', 'item'] = '기타'
df.loc[df['item'] == '옴마스트레페스', 'item'] = '기타'
df.loc[df['item'] == '기타 냉동연육 외 기타', 'item'] = '기타'
df.loc[df['item'] == '갑각류/연체동물/수생동물의', 'item'] = '갑각류'
df.loc[df['item'] == '가리비과의 조개', 'item'] = '조개'
df.loc[df['item'] == '넙치류', 'item'] = '넙치'
df.loc[df['item'] == '기타 넙치류', 'item'] = '넙치'

df.loc[df['item'] == '어류의 수우프/ 브로드와 수우프 브로드 제조용 조제품', 'item'] = '어류조제품'
df.loc[df['item'] == '암염', 'item'] = '소금'
df.loc[df['item'] == '넙치류', 'item'] = '넙치'
df.loc[df['item'] == '어류/갑각류/연체동물/수행동', 'item'] = '갑각류'
df.loc[df['item'] == '새조개', 'item'] = '조개'
df.loc[df['item'] == '어류외기타 분.조분 및 펠리트', 'item'] = '기타'

df.loc[df['item'] == '기타의 새우류의 기타', 'item'] = '새우류'
df.loc[df['item'] == '꽁치[콜로라비스 사이라', 'item'] = '꽁치'
df.loc[df['item'] == '태평양 연어', 'item'] = '연어'
df.loc[df['item'] == '건조한 것', 'item'] = '기타'
df.loc[df['item'] == '어류의 분.조분 및 펠리트', 'item'] = '조분'


# In[15]:


amount_table = df.pivot_table(values = 'amount_dollar', index = ['nat', 'ex_im'], aggfunc = 'sum')


# In[16]:


top_list = ['중국', '러시아', '베트남', '일본', '노르웨이', '미국', '카나다', '태국', '페루', '칠레', '대만']


# In[17]:


amount_table = amount_table.reset_index()


# In[18]:


amount_table_top = amount_table[amount_table['nat'].isin(top_list)].sort_values(by=['nat', 'amount_dollar'], ascending=False)


# In[19]:


amount_table_top


# In[20]:


temp_list = []
for item in df['zone']:
    for i in item.split('/'):
        temp_list.append(i)
temp_list_set = set(temp_list)
temp_list_set


# In[21]:


for item in temp_list_set:
    df[f"{item}"] = df['zone'].str.contains(item)


# In[22]:



df.columns = ['ex_im', 'nat', 'zone', 'item', 'item_weight', 'amount_dollar', 'item_price', 'EU', 'NAFTA', 'KOR-CHI-JAP', 'EFTA', 'independent', 'ASEAN', 'MERCOSUR', 'EAEU', 'TPP', 'GCC', 'RCEP', 'OECD','KOR-CentralAmerica-FTA', 'CPTPP', 'APEC']


# In[23]:


df.head(2)


# In[ ]:




