import boto3
from dotenv import find_dotenv, load_dotenv
import os
import mimetypes
import urllib

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


def upload_file(file_name, bucket, user_id):
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get('S3_KEY'),
                             aws_secret_access_key=os.environ.get('S3_SECRET'))
    file_path = url = urllib.parse.quote_plus(user_id+'/'+file_name)
    response = s3_client.upload_file(
        f"uploads/{file_name}",
        bucket,
        file_path,
        ExtraArgs={'ContentType': mimetypes.MimeTypes().guess_type(file_name)[0]})
    return response


def list_files(bucket, user_id):
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get('S3_KEY'),
                             aws_secret_access_key=os.environ.get('S3_SECRET'))

    public_urls = []
    folder = user_id+'/'
    try:
        for item in s3_client.list_objects(Bucket=bucket, Prefix=folder)['Contents']:
            url = "https://"+bucket+".s3.amazonaws.com/"+folder+item['Key']
            url = urllib.parse.quote_plus(url)
            filename = item['Key'].split('/')[-1]
            public_urls.append([url, filename])
    except Exception as e:
        pass
    return public_urls
