import json
import boto3
from datetime import datetime

# assign s3
s3 = boto3.resource('s3')

print('*Loading lambda: parrot')

def lambda_handler(event, context):
    # Read data
    body = event["body"]
    print('data:', body)
    
    # assign file
    bucket = 'moriaki-cs-bucket-231030'
    key = 'test_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.txt'
    file_contents = 'Lambda test'
    
    obj = s3.Object(bucket,key)
    obj.put(Body=file_contents)

    return {
        # 'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body':body
    }
