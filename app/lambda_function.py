import json
from app.src.point_query_use_case import execute


def handler(event, context):
    print(context)
    try:
        body = json.loads(event['body'])
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON'})
        }

    if 'matricula' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing matricula'})
        }

    matricula = body['matricula']
    execute(matricula)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': f'Matrícula {matricula} processada com sucesso!'})
    }
