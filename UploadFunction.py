import json
import boto3

s3 = boto3.resource('s3')

# assign bucket-name
BUCKET_NAME = 'moriaki-cs-bucket-231030'

def lambda_handler(event, context):
    # get request-id
    request_id = context.aws_request_id

    # assign bucket-name and object-name
    bucket = s3.Bucket(BUCKET_NAME)
    object_key_name = f"{request_id}.json"

    # generate object
    obj = bucket.Object(object_key_name)

    # upload the json data to the bucket
    json_data = event
    r = obj.put(Body = json.dumps(json_data))

    return {
        'request_id': request_id,
        'statusCode': 200,
    }