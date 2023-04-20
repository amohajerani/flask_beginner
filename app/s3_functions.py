import boto3
from dotenv import find_dotenv, load_dotenv
import os

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


def upload_file(file_name, bucket):
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get('S3_KEY'),
                             aws_secret_access_key=os.environ.get('S3_SECRET'))
    response = s3_client.upload_file(
        f"uploads/{file_name}", bucket, file_name, ExtraArgs={'ContentType': 'image/jpeg'})
    return response


def list_files(bucket):
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get('S3_KEY'),
                             aws_secret_access_key=os.environ.get('S3_SECRET'))

    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            url = "https://"+bucket+".s3.amazonaws.com/"+item['Key']
            public_urls.append([url, item['Key']])
    except Exception as e:
        pass
    print("[INFO] : The contents inside show_image = ", public_urls)
    return public_urls
