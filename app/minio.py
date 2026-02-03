from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
import os

load_dotenv()

def connect_minio():
    client = Minio(
        os.getenv("MINIO_URL"),
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=os.getenv("MINIO_SECURE")
    )
    return client


def download_image_minio(client, bucket, object_name, save_path):
    try:
        client.fget_object(bucket, object_name, save_path)
        print(f"Đã tải về: {save_path}")
    except S3Error as e:
        print("Lỗi MinIO:", e)