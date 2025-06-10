from rest_framework import serializers

from .models import ImageModel, ImageProcessingResults

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

