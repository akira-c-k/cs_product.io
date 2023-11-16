import json

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    if 'body' in event and event['body']:
        body_str = event["body"]

        # JSON文字列を辞書に変換
        body = json.loads(body_str)

        # keywordとactionsを取得（存在する場合）
        keyword = body.get("keyword", "")
        actions = body.get("actions", [])

        # 結果を出力（または他の処理を実施）
        print("Keyword:", keyword)
        print("Actions:", actions)
        for action in actions:
            print(action['action'])
            print(action['timestamp'])
            print(action['coordinates'])
            print(action['coordinates']['x'])
            print(action['coordinates']['y'])
    else:
        # bodyフィールドが存在しない場合の処理
        print("Bodyが存在しません。")
        
    # TODO implement
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(event)
    }