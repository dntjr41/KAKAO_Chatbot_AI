# 네이버 CLOVA 감정분석 API 이용
# https://medium.com/naver-cloud-platform/%EC%9D%B4%EB%A0%87%EA%B2%8C-%EC%82%AC%EC%9A%A9%ED%95%98%EC%84%B8%EC%9A%94-%ED%85%8D%EC%8A%A4%ED%8A%B8-%EA%B0%90%EC%A0%95-%EB%B6%84%EC%84%9D-%EC%84%9C%EB%B9%84%EC%8A%A4-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-clova-sentiment-%ED%99%9C%EC%9A%A9%EA%B8%B0-5d9db7b0209b

import sys
import requests
import json

client_id = "hhckdn2v5m"
client_secret = "5KfiupCfN3iJxVnDj2Be7L1xixED5ZHStlZObpMi"
url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"

headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json"
}

content = "여기에 문장이 들어가야함"
data = {
    "content": content
}

print(json.dumps(data, indent=4, sort_keys=True))
response = requests.post(url, data=json.dumps(data), headers=headers)
rescode = response.status_code

if (rescode == 200):
    print (response.text)

else:
    print("Error : " + response.test)