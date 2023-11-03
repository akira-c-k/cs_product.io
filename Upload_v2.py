import json
import boto3
from datetime import datetime

# assign s3
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    # Read data
    body = event['body']
    data = json.loads(body)
    key = data['key']
    x = data['x']
    y = data['y']

    # assign file
    bucket_name = 'moriaki-cs-bucket-231030'
    file_name = str(key) + '.json'
    file_content = {
        'x': x,
        'y': y
    }
    file_content = json.dumps(file_content)
    
    obj = s3.Object(bucket_name, file_name)
    obj.put(Body=file_content)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body':body
    }