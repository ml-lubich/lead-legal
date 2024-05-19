import boto3
from botocore.exceptions import NoCredentialsError
import os

BUCKET_NAME = 'lead-legal-db'

def create_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name='us-east-2'
    )

def upload_file_to_s3(client, file, object_name):
    try:
        client.upload_fileobj(file, BUCKET_NAME, object_name)
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_name}"
    except NoCredentialsError:
        print('Credentials not available')
        return None

def download_file_from_s3(s3_url, local_file_name):
    s3 = boto3.client('s3')
    key = '/'.join(s3_url.split('/')[3:])
    print('===\n',key)
    try:
        s3.download_file(BUCKET_NAME, key, local_file_name)
        print(f"Downloaded {key} to {local_file_name}")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"Failed to download file: {e}")

