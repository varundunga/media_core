from minio import Minio
import os
from io import BytesIO
import logging
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_core.settings')

from django.conf import settings

logger = logging.getLogger(__name__)

minio_client = Minio(
    f"{settings.MINIO_HOST}:{str(settings.MINIO_PORT)}",
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)

def download_file(bucket_name, object_name, download_path):
    """Download a file from MinIO."""
    minio_client.fget_object(bucket_name, object_name, download_path)

def upload_file(bucket_name, object_name, file_data):
    """Upload a file-like object (BytesIO) to MinIO."""
    try:
        # Ensure file_data is a BytesIO object
        if isinstance(file_data, BytesIO):
            file_data.seek(0)  # Ensure the pointer is at the beginning of the stream
            minio_client.put_object(
                bucket_name,
                object_name,
                file_data,
                length=file_data.getbuffer().nbytes,
                content_type="image/jpeg"  # Adjust content type based on the file type
            )
            logger.info(f"Uploaded {object_name} to bucket {bucket_name}")
        else:
            logger.error("Error: file_data is not a BytesIO object")
    except Exception as e:
        logger.exception(f"Error uploading file to MinIO: {str(e)}")

def list_objects(bucket_name, prefix=None):
    """List objects in a bucket."""
    return minio_client.list_objects(bucket_name, prefix=prefix, recursive=True)

def read_file(bucket_name, object_name):
    """Read a file from MinIO and return a file-like object."""
    try:
        response = minio_client.get_object(bucket_name, object_name)
        # Wrap the response in a BytesIO object to make it file-like
        file_stream = BytesIO(response.read())
        response.close()
        response.release_conn()
        return file_stream
    except Exception as e:
        logger.exception(f"Error reading file from MinIO: {str(e)}")
        return None