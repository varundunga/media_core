import logging
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, parsers, status, viewsets


from celery.result import AsyncResult

from .serializers import ImageSerializer, UploadImageSerializer
from .models import UploadImage
from .tasks import generate_thumbnail
from media_core import celery_app

logger = logging.getLogger(__name__)

# Create your views here.
@api_view(["POST"])
def process_image(request):
    logger.warning(request.body)
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

class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = UploadImage.objects.all()
    serializer_class = UploadImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
