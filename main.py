from flask import Flask, request, jsonify, render_template, send_file, Response
import os
import base64
import main

import pandas
import pymysql
from io import StringIO

import multiple_clustering
import multiple_prediction

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
output_path = '' # write your output path
app = Flask(__name__)
conn = pymysql.connect(host='localhost', port=3307, user='root', password='12345', db='enc')

@app.route("/")
def index():
    return "<h1>SurMoonVey ML service</h1>"

@app.route('/csv/<int:user_id>/<int:survey_id>', methods=['GET', 'POST'])
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

@app.route('/clustering/<int:user_id>/<int:survey_id>/', methods=['GET', 'POST'])
def multiple_cl(user_id=None, survey_id=None):
    data = request.get_json()

    sql = 'SELECT * FROM response where ', data
    result = pandas.read_sql_query(sql, conn)
    result.to_csv('result.csv', index=False)

    multiple_clustering()


@app.route('/prediction/<int:user_id>/<int:survey_id>/', methods=['GET', 'POST'])
def multiple_pr(user_id=None, survey_id=None):
    data = request.get_json()

    sql = 'SELECT * FROM response where ', data
    result = pandas.read_sql_query(sql, conn)
    result.to_csv('result.csv', index=False)

    multiple_prediction()



if __name__ == "__main__":
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(threaded=True, host='127.0.0.1', port=8081)
    ALLOWED_HOSTS = ["*"]