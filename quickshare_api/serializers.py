from rest_framework import serializers
from .models import Image, List, ListElement

class QuickshareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image_id","image_name","upload_data"]

class QuickshareSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ["list_id","title","descrizione","create_data"]

# class QuickshareSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ListElement
#         fields = ["list_element_id","description","do"]