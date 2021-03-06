import boto3, botocore
from config import S3_ACCESS, S3_SECRET, S3_BUCKET, S3_LOCATION, S3_REGION

s3 = boto3.client(
  "s3",
  aws_access_key_id = S3_ACCESS,
  aws_secret_access_key = S3_SECRET
)

def upload_file_to_s3(file, bucket_name, acl="public-read"):
  try:
    s3.upload_fileobj(
      file,
      bucket_name,
      file.filename,
      ExtraArgs={
        "ACL": acl,
        "ContentType": file.content_type
      }
    )
  except Exception as e:
    print("Something Happened: ", e)
    return e
  return file.filename

def s3_url(filename):
  return f"https://{S3_REGION}.amazonaws.com/{S3_BUCKET}/{filename}"

def map_to_s3(images):
  return list(map(lambda img: img.remote_url, images))