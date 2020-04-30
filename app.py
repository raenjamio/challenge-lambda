from flask import Flask, request
from flask import json
import boto3
import logging
import os
import pymysql
import sys
from boto3.dynamodb.conditions import Key, Attr

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_DYNAMO_DB'])

rds_host = os.environ['DB_HOST']
rds_user = os.environ['DB_USER']
rds_password = os.environ['DB_PASSWORD']
rds_database = os.environ['DB_DATABASE']


logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=rds_user, passwd=rds_password, db=rds_database, connect_timeout=5)
except Exception as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


@app.route('/')
def hello_world():
    response = app.response_class(
        response=json.dumps({"hello": "lambda"}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/dynamoDb', methods=['POST'])
def create_customer():
    req_data = request.get_json()
    response = table.put_item(
        Item={
            'email': req_data['email'],
            'name': req_data['name']
        }
    )
    return app.response_class(
        response=json.dumps(response),
        status=201,
        mimetype='application/json'
    )


@app.route('/dynamoDb', methods=['GET'])
def get_customers():
    response = table.scan()

    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )


@app.route('/rds', methods=['GET'])
def get_challenges_rds():
    records = run_query("select * from challenge")

    return app.response_class(
        response=json.dumps(records),
        status=200,
        mimetype='application/json'
    )


@app.route('/rds', methods=['POST'])
def create_challenge():
    logger.info("rds challenge")

    req_data = request.get_json()
    query = "INSERT INTO challenge (name, description) VALUES ('%s', '%s')""" % (req_data["name"], req_data["description"])

    run_query(query)
    return app.response_class(
        response=json.dumps(req_data),
        status=201,
        mimetype='application/json'
    )


def run_query(query=''):
    cursor = conn.cursor()
    cursor.execute(query)

    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()
    else:
        conn.commit()
        data = None

    cursor.close()
    return data


if __name__ == '__main__':
    app.run()
