import json
import boto3
from botocore.exceptions import ClientError

bucket_name = ''  # S3バケット名を設定

# API Gatewayのルールに則った成功の response を生成する
def create_response(body, **kwargs):
    origin  = '*'
    methods = 'GET'
    statusCode = 200

    for k, v in kwargs.items():
        if k == 'origin'  : origin  = v
        if k == 'methods' : methods = v 
        if k == 'statusCode':statusCode = v

    headers = {
        'Access-Control-Allow-Headers' : 'Content-Type',
        'Access-Control-Allow-Origin'  : origin,
        'Access-Control-Allow-Methods' : methods
    }

    return {
        'isBase64Encoded': False,
        'statusCode'     : statusCode,
        'headers'        : headers,
        'body'           : json.dumps(body)
    }

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))

    if 'body' in event and event['body']:
        body_str = event["body"]

        # JSON文字列を辞書に変換
        body = json.loads(body_str)

        # keywordとactionsを取得（存在する場合）
        keyword = body.get("keyword", "")

        # 結果を出力（または他の処理を実施）
        print("Keyword:", keyword)
        
        s3 = boto3.client('s3')
        
        try:
            # S3バケットからファイルを取得
            response = s3.get_object(Bucket=bucket_name, Key=f'{keyword}.json')
            file_content = response['Body'].read().decode('utf-8')
            json_content = json.loads(file_content)
    

            return create_response(
                json_content,
                methods='POST'
            )
            
        except ClientError as e:
            # エラー処理（ファイルが見つからないなど）
            print(e)
            return create_response(
                {"message": "File not found"},
                methods='POST',
                statusCode = 404
            )
            
    elif event['httpMethod'] == 'OPTIONS':
        print('handle the options method.')
    
        return create_response(
            { 'message': 'successfully: called options method.' },
            methods='OPTIONS,POST,GET'
        )
        
    else:
        # bodyフィールドが存在しない場合の処理
        print("Bodyが存在しません。")
        return create_response(
            {"message": "Body not found"},
            method = 'POST',
            statusCode = 400
        )