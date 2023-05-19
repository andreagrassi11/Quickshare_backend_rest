from rest_framework import serializers
from .models import Image, List, ListElement

class QuickshareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id","image_name","upload_data"]

    class Meta:
        model = List
        fields = ["id","title","description"]

    class Meta:
        model = ListElement
        fields = ["id","title","description"]