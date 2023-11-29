import json
import boto3

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
        actions = body.get("actions", [])

        # S3に書き込む
        if keyword:  # keywordがある場合のみ処理を実施
            s3 = boto3.client('s3')

            # JSONデータを文字列に変換
            s3_data = json.dumps(body)

            # S3バケットにファイルを書き込む
            s3.put_object(Bucket=bucket_name, Key=f'{keyword}.json', Body=s3_data)

        # 結果を出力（または他の処理を実施）
        print("Keyword:", keyword)
        print("Actions:", actions)
        
        return create_response(
                body,
                methods='POST'
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
                {"message": "File not found"},
                methods='POST',
                statusCode = 404
            )
