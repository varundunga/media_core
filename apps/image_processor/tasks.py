from PIL import Image
import os
from io import BytesIO

from media_core import minio_utils, celery_app
from .serializers import ImageProcessingResultSerializer as ResultsSerializer
from .models import ImageModel

def save_result(result_data):
    serializer = ResultsSerializer(data=result_data)
    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(f"Failed to save result: {serializer.errors}")

@celery_app.task
def generate_thumbnail(image_id, trgt_bucket: str, size=(128, 128)) -> str:
    image = ImageModel.objects.filter(id=image_id).first()
    if not image:
        raise Exception(f"Image with ID {image_id} not found.")
    try:
        img_stream = minio_utils.read_file(image.blob_bucket, image.blob_file_name)
        if not img_stream:
            error = f"File {image.blob_file_name} not found in bucket {image.blob_bucket}"
            result_data = {
                "image": image.id,
                "blob_bucket": trgt_bucket,
                "result": "FAILED",
                "error": error
            }
            save_result(result_data)
            return error
        
        # Open the image using Pillow
        img = Image.open(img_stream)
        img.thumbnail(size)
        
        # Save the thumbnail to an in-memory buffer
        thumbnail_buffer = BytesIO()
        img.save(thumbnail_buffer, format="PNG")
        thumbnail_buffer.seek(0)  # Reset buffer pointer to the beginning
        
        # Upload the thumbnail directly to the target bucket in MinIO
        thumbnail_name = f"{os.path.splitext(image.blob_file_name)[0]}_thumbnail.jpg"
        minio_utils.upload_file(trgt_bucket, thumbnail_name, thumbnail_buffer)
        thumbnail_buffer.close()
        result_data = {
            "image": image.id,
            "blob_bucket": trgt_bucket,
            "blob_file_name": thumbnail_name,
            "result": "SUCCESS",
            "error": None
        }
        save_result(result_data)
        return f"Thumbnail uploaded to bucket {trgt_bucket} as {thumbnail_name}"
    except Exception as e:
        error = f"Error generating thumbnail: {str(e)}"
        result_data = {
            "image": image.id,
            "blob_bucket": trgt_bucket,
            "result": "FAILED",
            "error": error
        }
        save_result(result_data)
        return error
