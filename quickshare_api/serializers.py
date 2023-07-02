from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
import base64
from drf_extra_fields.fields import Base64ImageField
from .validators import validate_password

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(validators=[validate_password])

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name','email','username','password')
        extra_kwargs = {
            'password':{'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],  
            first_name = validated_data['first_name'],  
            last_name = validated_data['last_name'],
            email = validated_data['email']
        )
        return user

class UserGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name','username', 'email']

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Image serializer
class ImagePostSerializer(serializers.ModelSerializer):
    
    allowed = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset= User.objects.all()
    )

    class Meta:
        model = Image
        fields = ['image_id','data','upload_data', 'allowed']

    def create(self, validated_data):
        related_models_data = validated_data.pop('allowed')

        image = Image.objects.create(**validated_data)
        image.allowed.set(related_models_data)
        image.save()
        return image

    def update(self, instance, validated_data):
        user_id = validated_data.pop('allowed')
        related_models = instance.allowed.all()
        related_models = list(related_models)
        related_models.extend(user_id)
        instance.allowed.set(related_models)
        instance.save()
        return instance
    
class ImageGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'

# Note serializer
class NotePostSerializer(serializers.ModelSerializer):
    
    allowed = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset= User.objects.all()
    )
     
    class Meta:
        model = Note
        fields = '__all__'

    def create(self, validated_data):
        related_models_data = validated_data.pop('allowed')
        note = Note.objects.create(**validated_data)
        note.allowed.set(related_models_data)
        note.save()
        return note

    def update(self, instance, validated_data):
        user_id = validated_data.pop('allowed')
        related_models = instance.allowed.all()
        related_models = list(related_models)
        related_models.extend(user_id)
        instance.allowed.set(related_models)
        instance.title = validated_data.get('title')
        instance.body = validated_data.get('body')
        instance.save()
        return instance
    
class NoteGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = '__all__'

# List serializer
class ListPostSerializer(serializers.ModelSerializer):
    
    allowed = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset= User.objects.all()
    )
     
    class Meta:
        model = List
        fields = '__all__'

    def create(self, validated_data):
        related_models_data = validated_data.pop('allowed')
        list = List.objects.create(**validated_data)
        list.allowed.set(related_models_data)
        list.save()
        return list

    def update(self, instance, validated_data):
        user_id = validated_data.pop('allowed')
        related_models = instance.allowed.all()
        related_models = list(related_models)
        related_models.extend(user_id)
        instance.allowed.set(related_models)
        instance.title = validated_data.get('title')
        instance.save()
        return instance
    
class ListGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = List
        fields = '__all__'
    
class ListElementPutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ListElement
        fields = ['do']

    def update(self, instance, validated_data):
        instance.do = validated_data.get('do')
        instance.save()
        return instance
    
class ListElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ListElement
        fields = '__all__'

# Financial serializer
class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expenses
        fields = '__all__'

class IncomeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Income
        fields = '__all__'

# Calendar serializer
class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = '__all__'

# Chat serializer
class ChatSerializer(serializers.ModelSerializer):

    allowed = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset= User.objects.all()
    )

    class Meta:
        model = Message
        fields = '__all__'
    
    def create(self, validated_data):
        related_models_data = validated_data.pop('allowed')
        note = Message.objects.create(**validated_data)
        note.allowed.set(related_models_data)
        note.save()
        return note
    
class ChatPutSerializer(serializers.ModelSerializer):

    allowed = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset= User.objects.all()
    )

    class Meta:
        model = Message
        fields = ['allowed']
    
    def update(self, instance, validated_data):
        user_id = validated_data.pop('allowed')
        related_models = instance.allowed.all()
        related_models = list(related_models)
        related_models.extend(user_id)
        instance.allowed.set(related_models)
        instance.save()
        return instance
    

class SearchNotesGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ['note_id']