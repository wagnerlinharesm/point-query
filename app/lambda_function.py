import json
import base64
from app.src.point_query_use_case import execute


def handler(event):
    try:
        username = extract_token(event)
        if not username:
            raise ValueError('Username not found in token')
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    result = execute(username)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'{result}'})
    }


def extract_token(event):
    token = event['headers'].get('Authorization', '').split(' ')[1]
    payload = token.split('.')[1]
    payload += '=' * ((4 - len(payload) % 4) % 4)
    decoded_payload = base64.b64decode(payload).decode('utf-8')
    token_payload = json.loads(decoded_payload)
    username = token_payload.get('cognito:username')
    return username
