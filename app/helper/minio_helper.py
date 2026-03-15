import io
from app.minio import minio_client

def sync_minio_upload(file_data, object_name, content_type):
    minio_client.put_object(
        "img",
        object_name,
        data=io.BytesIO(file_data),
        length=len(file_data),
        content_type=content_type
    )