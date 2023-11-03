import json
import boto3

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    # read data
    body = event['body']
    data = json.loads(body)
    key = data['key']
    
    # assgin bucket_name and object_key
    bucket_name = 'moriaki-cs-bucket-231030'
    object_key = key + '.json'
    
    bucket = s3.Bucket(bucket_name)
    obj = bucket.Object(object_key)

    response = obj.get()    
    body = response['Body'].read()

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body':body
    }