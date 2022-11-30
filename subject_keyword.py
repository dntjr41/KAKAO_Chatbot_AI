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
import pandas as pd

client_secret = "f2bfcd561f6cb2b831e05c72d9b1f1c3"
url = "https://60520ecf-9f3b-4709-a575-dd199defbcf4.api.kr-central-1.kakaoi.io/ai/nlp/afc1cf3b457f45889aedb98a80c1209b"
language = "ko"

headers = {
    "x-api-key": client_secret,
    "Content-Type": "application/json"
}

def subject_keyword(params):

    df = pd.json_normalize(params)
    df = df[['questionId', 'questionOrder', 'type', 'title']]
    df_answer = pd.json_normalize(params, record_path=['answers'])
    df_answer = df_answer[['value']]
    df_use = pd.concat([df, df_answer], axis=1)
    df_use = df_use[df_use['type'] == 4]

    list_questionId = df_use['questionId'].values.tolist()
    list_questionId = list(set(list_questionId))

    # dataframe 전체 확인
    # pd.set_option("display.max_rows", None, "display.max_columns", None)
    # print(df_use)
    # print('list')
    # print(list_questionId)

    keyword_result = pd.DataFrame(index=['questionId', 'title', 'keyword', 'weight'])

    temp_content = []
    temp_title = ""

    for k in list_questionId:
        for h in range(len(df_use)):
            df_temp = df_use.iloc[h, :]
            if df_temp['questionId'] == k:
                temp_content.append(df_temp['value'])
                temp_title = df_temp['title']

        content = temp_content
        data = {
            "sentences": content
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)
        rescode = response.status_code

        print(response)

        if (rescode == 200):
            print(response.text)

        else:
            print("Error : " + response.text)

        use_temp = json.loads(response.text)
        use_temp2 = pd.DataFrame(use_temp['result'])
        temp_key = use_temp2['keyword'].to_string()[5:]
        temp_weight = use_temp2['weight'].to_string()[5:]

        keyword_result = keyword_result.append({'questionId':k, 'title':temp_title, 'keyword': temp_key, 'weight':temp_weight}, ignore_index=True)
        temp_content = []
        temp_title = ""

    keyword_result = keyword_result.dropna(axis=0)
    keyword_result = keyword_result.reset_index(drop=True)

    return keyword_result