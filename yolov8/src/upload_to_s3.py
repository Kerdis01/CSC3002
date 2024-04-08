from .credentials import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import os
import boto3

def upload_to_s3(bucket_name, file_path, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
        os.remove(file_path)
    except Exception as e:
        print(f"Failed to upload {file_path} to {bucket_name}/{object_name}.")
        print(e)
