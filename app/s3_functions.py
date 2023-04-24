import boto3
from dotenv import find_dotenv, load_dotenv
import os
import mimetypes

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


def url_friendly(word):
    word = word.replace('|', '_')
    return word


def upload_file(file_location, bucket, username, filename):
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get('S3_KEY'),
                             aws_secret_access_key=os.environ.get('S3_SECRET'))
    file_path = username+'/'+filename
    response = s3_client.upload_file(
        file_location,
        bucket,
        file_path,
        ExtraArgs={'ContentType': mimetypes.MimeTypes().guess_type(filename)[0]})
    return response


def get_file_names(bucket, username):
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get('S3_KEY'),
                             aws_secret_access_key=os.environ.get('S3_SECRET'))

    files = []
    folder = username+'/'
    try:
        for item in s3_client.list_objects(Bucket=bucket, Prefix=folder)['Contents']:
            filename = item['Key'].split('/')[-1]
            files.append(filename)
    except Exception as e:
        pass
    return files


def get_file_obj(filepath, bucket):
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get('S3_KEY'),
                             aws_secret_access_key=os.environ.get('S3_SECRET'))
    return s3_client.get_object(Bucket=bucket, Key=filepath, ResponseContentType=mimetypes.MimeTypes().guess_type(filepath)[0])
