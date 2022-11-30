import pandas as pd
from flask import Flask, request, jsonify, render_template, send_file, Response
import os
import base64
from werkzeug.serving import WSGIRequestHandler

import pandas
import pymysql
from io import StringIO
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, reqparse

# import multiple_clustering
# import multiple_prediction

import subject_keyword
import subject_sentiment

# import py_eureka_client.eureka_client as eureka_client

rest_port = 8087

'''
eureka_client.init(eureka_server="http://localhost:8761/eureka",
                   app_name="surmoonvey-ai",
                   instance_port=rest_port)
'''

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
output_path = '' # write your output path
app = Flask(__name__)
CORS(app, supports_credentials=True)
api = Api(app, version='1.0', title='Surmoonvey AI Document', description='Swagger 문서', doc="/api-docs")

# 테스트
test_api = api.namespace('test', description='조회 API')


# conn = pymysql.connect(host='localhost', port=3307, user='root', password='12345', db='enc')
conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='survey')

@app.route("/")
def index():
    return "<h1>SurMoonVey ML service</h1>"

# Return Dataframe 형태
# questionId sentiment keyword
# 이 데이터프레임을 json으로 변환하여 다시 react로 전송

@app.route('/react_to_flask', methods=['POST'])
def react_to_flask():
    print(request.is_json)
    params = request.get_json()
    print(params)

    result = pandas.DataFrame()
    subject_se = subject_sentiment.subject_sentiment(params)
    subject_ke = subject_keyword.subject_keyword(params)

    pandas.set_option("display.max_rows", None, "display.max_columns", None)
    result = pd.merge(subject_se, subject_ke)
    print(result)

    return result.to_json(orient='records')

'''
@app.route('api/csv/<int:survey_id>', methods=['GET', 'POST'])
def csv(user_id=None, survey_id=None):
    output_stream = StringIO()

    sql = "select (%d) from response" % survey_id
    result = pandas.read_sql_query(sql, conn)
    #result.to_csv('result.csv', index=False)
    result.to_csv(output_stream)

    response = Response(
            output_stream.getvalue(),
            mimetype='text/csv',
            content_type='application/octet-stream',
        )
    response.headers["Content-Disposition"] = "attachment; filename=Survey_result.csv"
    return response

"""
    return send_file('result.csv',
                     mimetype='text/csv',
                     attachment_filename='Survey_result.csv',
                     as_attachment=True)
"""

"""
Json 예상도
key_question : 1
select_question : [ 2, 3, 4 ...] 
"""

@app.route('api/clustering/<int:survey_id>/', methods=['GET', 'POST'])
def multiple_cl(user_id=None, survey_id=None):
    data = request.get_json()

    sql = 'SELECT * FROM response where ', data
    result = pandas.read_sql_query(sql, conn)
    result.to_csv('result.csv', index=False)

    # multiple_clustering()


@app.route('api/prediction/<int:survey_id>/', methods=['GET', 'POST'])
def multiple_pr(user_id=None, survey_id=None):
    data = request.get_json()

    sql = 'SELECT * FROM response where ', data
    result = pandas.read_sql_query(sql, conn)
    result.to_csv('result.csv', index=False)

    # multiple_prediction()
'''

if __name__ == "__main__":
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(threaded=True, host='127.0.0.1', port=rest_port)
    ALLOWED_HOSTS = ["*"]