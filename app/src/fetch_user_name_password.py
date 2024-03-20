import boto3
import json


def fetch_username_password(secret_name):
    client = boto3.client('secretsmanager')

    try:
        response = client.get_secret_value(SecretId=secret_name)

        secret = response['SecretString']

        secret_dict = json.loads(secret)

        return secret_dict['username'], secret_dict['password']
    except Exception as e:
        print(f"Error fetching secret {secret_name}: {e}")
        return None, None

