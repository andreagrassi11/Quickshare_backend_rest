from rest_framework import serializers
from .models import Image

class QuickshareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id","image_name","upload_data"]