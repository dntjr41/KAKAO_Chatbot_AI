# 카카오 NLP 키워드 추출 사용
'''
curl -L -X POST '{API Endpoint URL}' \
 -H 'x-api-key: {API Key}' \
 -H 'Content-Type: application/json' \
 -d '{
    "sentences": [
        "기축 통화는 국제 거래에 결제 수단으로 통용되고 환율 결정에 기준이 되는 통화이다.",
        "1960년 트리핀 교수는 브레턴우즈 체제 에서의 기축 통화인 달러화의 구조적 모순을 지적했다.",
        "한 국가의 재화와 서비스의 수출입 간 차이인 경상 수지는 수입이 수출을 초과하면 적자이고, 수출이 수입을 초과하면 흑자이다."
    ],
    "lang": "ko"
  }'
'''

import sys
import requests
import json

client_secret = "f2bfcd561f6cb2b831e05c72d9b1f1c3"
url = "https://60520ecf-9f3b-4709-a575-dd199defbcf4.api.kr-central-1.kakaoi.io/ai/nlp/afc1cf3b457f45889aedb98a80c1209b"
language = "ko"


'''
curl -L -X POST 'https://60520ecf-9f3b-4709-a575-dd199defbcf4.api.kr-central-1.kakaoi.io/ai/nlp/afc1cf3b457f45889aedb98a80c1209b' \
    -H 'x-api-key: f2bfcd561f6cb2b831e05c72d9b1f1c3' \
    -H 'Content-Type: application/json' \
    -d '{
       "sentences": [

       ],
       "lang": "ko"
    }'

'''
