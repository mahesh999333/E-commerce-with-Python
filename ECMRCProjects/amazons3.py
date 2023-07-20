# import os
# import boto3
# import botocore
# import requests
# from io import BytesIO
# from django.conf import settings
# import datetime


# class AmazonS3Helper:
#     def __init__(self):
#         self.bucket_name = "lendendocs"
#         self.access_key = "AKIAJKZFYGY2CFB6WF6Q"
#         self.secret_key = "+e0N+bXyLFDrO4k8gHI0ICdRjT\/8\/ROlg533hzmw"
#         self.s3_bucket_postfix = "media/documents"
#         self.s3_client = None

#     def initialize_s3_client(self):
#         session = boto3.Session(
#             aws_access_key_id=self.access_key,
#             aws_secret_access_key=self.secret_key
#         )
#         print("Amazon S3 coonection established.")
#         self.s3_client = session.client('s3', region_name='ap-south-1')

#     def upload_to_s3(self, file, file_name, bytes_data):
#         folder_location = self.get_s3_folder_name()
#         s3_key = f"{folder_location}/{file_name}"

#         try:
#             self.s3_client.put_object(
#                 Body=bytes_data,
#                 Bucket=self.bucket_name,
#                 Key=s3_key
#             )
#             return_bucket_file_name = f"{self.bucket_name}/{s3_key}"
#             return return_bucket_file_name
#         except botocore.exceptions.BotoCoreError as e:
#             raise Exception("Error while uploading to S3") from e
#         finally:
#             os.remove(file.name)

#     def download_file_from_s3(self, s3_url, file_name):
#         file_path = os.path.join(os.getcwd(), file_name)
#         response = requests.get(s3_url)

#         with open(file_path, 'wb') as f:
#             f.write(response.content)

#         return file_path

#     def get_s3_folder_name(self):
#         current_date = datetime.datetime.now().strftime("%Y/%m/%d")
#         return f"{self.s3_bucket_postfix}/{current_date}"




# ---------------------------------------------------------------------------


import logging
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from django.conf import settings
import uuid
import requests
import os
from datetime import datetime
import tempfile
logger = logging.getLogger('django')
# Version 1
def generate_temp_file_from_request_file(file, suffix=None):
    if suffix:
        tmp = tempfile.NamedTemporaryFile(suffix=suffix)
    else:
        tmp = tempfile.NamedTemporaryFile()
    for chunk in file.chunks():
        tmp.write(chunk)
    return tmp


def get_24_char_uuid():
    uid = uuid.uuid4().hex
    for i in range(0, 8):
        uid = uid[:i] + uid[i + 1:]
    return uid.upper()


class FileUtils:
    def get_filepath_with_name(self, name):
        date = datetime.strftime(datetime.now(), "%Y/%m/%d/")
        ext = name.split('.')[-1]
        return 'media/documents/' + date + get_24_char_uuid() + "." + ext
    
    
file_utils = FileUtils()
logger = logging.getLogger('django')
aws_config = settings.AWS_CONFIGURATION


def guess_mime_type(file_name):
    if '.pdf' in str(file_name).lower():
        return 'application/pdf'
    return None


def upload_to_s3(local_file, s3_file,
                 s3_bucket_name=
                 aws_config['AWS_STORAGE_BUCKET_NAME']):
    try:
        client = boto3.client(
            's3', aws_access_key_id=aws_config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=aws_config['AWS_SECRET_ACCESS_KEY'],
            config=Config(signature_version='s3v4'),
            region_name=aws_config['AWS_REGION']
        )
    except ClientError as err:
        logger.exception("Failed to create boto3 client", err)
        raise err
    try:
        extra_args = {
            'ACL': 'public-read',
        }
        mimetype = guess_mime_type(local_file)
        if mimetype:
            extra_args['ContentType'] = mimetype
        response = client.upload_file(
            local_file,
            s3_bucket_name,
            s3_file,
            ExtraArgs=extra_args
        )
        s3_url = f"https://{aws_config['AWS_S3_HOST']}/{s3_bucket_name}/"
        file_url = f'{s3_url}{s3_file}'
        return file_url
    except ClientError as err:
        logger.exception("Failed to upload artifact to S3", err)
        raise err
    except IOError as err:
        logger.exception("Failed to access artifact.zip in this directory", err)
        raise err
    
    
def fetch_from_s3(file_key, file_object,
                  s3_bucket_name=aws_config['AWS_STORAGE_BUCKET_NAME']):
    try:
        client = boto3.client(
            's3', aws_access_key_id=aws_config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=aws_config['AWS_SECRET_ACCESS_KEY'],
            config=Config(signature_version='s3v4'),
            region_name=aws_config['AWS_REGION']
        )
    except ClientError as err:
        logger.exception("Failed to create boto3 client", err)
        raise err
    try:
        return client.download_fileobj(
            Bucket=s3_bucket_name,
            Key=file_key,
            Fileobj=file_object)
    except Exception as err:
        logger.exception("Failed to fetch file", err)
        raise err
def upload_in_memory_file_to_s3(file):
    temp_file = generate_temp_file_from_request_file(file)
    s3_folder_location = file_utils.get_filepath_with_name(
        str(file))
    return upload_to_s3(temp_file.name, s3_folder_location)
