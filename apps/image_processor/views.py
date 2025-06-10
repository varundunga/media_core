from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from celery.result import AsyncResult

from .serializers import ImageSerializer
from .tasks import generate_thumbnail
from media_core import celery_app


# Create your views here.
@api_view(["POST"])
def process_image(request):
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        task_result: AsyncResult = generate_thumbnail.delay(
            instance.id,
            "thumbnails",
            size=(128, 128),
        )
        return Response(
            {
                "image": serializer.data,
                "thumbnail": {
                    "task_id": task_result.id,
                    "task_status": task_result.status,
                },
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_task_status(request, task_id):
    task_result: AsyncResult = celery_app.AsyncResult(task_id)
    if not task_result:
        return Response(
            {"error": "Task not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response(
        {
            "task_id": task_id,
            "task_status": task_result.state,
            "result": task_result.result,
        },
        status=status.HTTP_200_OK
    )
