# 네이버 CLOVA 감정분석 API 이용
# https://medium.com/naver-cloud-platform/%EC%9D%B4%EB%A0%87%EA%B2%8C-%EC%82%AC%EC%9A%A9%ED%95%98%EC%84%B8%EC%9A%94-%ED%85%8D%EC%8A%A4%ED%8A%B8-%EA%B0%90%EC%A0%95-%EB%B6%84%EC%84%9D-%EC%84%9C%EB%B9%84%EC%8A%A4-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-clova-sentiment-%ED%99%9C%EC%9A%A9%EA%B8%B0-5d9db7b0209b

import sys
import requests
import json
import pandas as pd

client_id = "hhckdn2v5m"
client_secret = "5KfiupCfN3iJxVnDj2Be7L1xixED5ZHStlZObpMi"
url = "https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"

headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json"
}

def subject_sentiment(params):

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

    sentiment_result = pd.DataFrame(index=['questionId', 'sentiment', 'negative', 'positive', 'neutral'])
    temp_content = ""

    for k in list_questionId:
        for h in range(len(df_use)):
            df_temp = df_use.iloc[h, :]
            if df_temp['questionId'] == k:
                temp_content = temp_content + " " + df_temp['value']

        content = temp_content
        data = {
            "content": content
        }

        # print(json.dumps(data, indent=4, sort_keys=True))
        response = requests.post(url, data=json.dumps(data), headers=headers)
        rescode = response.status_code

        if (rescode == 200):
            print(response.text)

        else:
            print("Error : " + response.text)

        use_temp = json.loads(response.text)
        use_temp2 = pd.DataFrame(use_temp['document'])
        confidence = use_temp2['confidence']

        temp_sent = use_temp2.drop_duplicates(['sentiment'])
        temp_sent = temp_sent.reset_index()
        temp_sent = temp_sent['sentiment'].to_string()[5:]
        temp_nega = confidence['negative']
        temp_posi = confidence['positive']
        temp_neut = confidence['neutral']

        print(temp_sent)

        sentiment_result = sentiment_result.append({'questionId':k, 'sentiment': temp_sent, 'negative': temp_nega,
                                                    'positive': temp_posi, 'neutral': temp_neut}, ignore_index=True)
        temp_content = ""

    sentiment_result = sentiment_result.dropna(axis=0)
    sentiment_result = sentiment_result.reset_index(drop=True)

    return sentiment_result