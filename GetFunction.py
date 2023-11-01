import json
import boto3

s3 = boto3.resource('s3')

# assign bucket-name
BUCKET_NAME = 'moriaki-cs-bucket-231030'

def lambda_handler(event, context):
    # get request-id
    request_id = event["request_id"]

    # assign bucket-name and object-name
    bucket = s3.Bucket(BUCKET_NAME)
    object_key_name = '{}.json'.format(request_id)

    # generate object
    obj = bucket.Object(object_key_name)

    try:
        # get data from json
        response = obj.get()    
        body = response['Body'].read()

        # change the data-type from json to dictionary
        json_data = json.loads(body.decode('utf-8'))
    except:
        print('指定したファイルは存在しません')
        json_data = {}

    return json_data