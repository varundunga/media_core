from rest_framework import serializers

from .models import ImageModel, ImageProcessingResults, UploadImage

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = '__all__'
    # def create(self, validated_data):
    #     return super().create(validated_data)
    
class ImageProcessingResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProcessingResults
        fields = '__all__'

class UploadImageSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    class Meta:
        model = UploadImage
        fields = ['file']
        