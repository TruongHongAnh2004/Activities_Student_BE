from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
import os

load_dotenv()

minio_client = Minio(
    "127.0.0.1:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)


# Ensure the bucket exists
if not minio_client.bucket_exists("img"):
    minio_client.make_bucket("img")

