from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import *
from .serializers import *
import datetime
from django.db.models import Q
from rest_framework import generics, permissions, mixins
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


# User API
class RegisterApi(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

# Image API    
class UserImageView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # Take all image for user
    def get(self, request, user_id, *args, **kwargs):
        ''' List all the image for given requested user '''
        images = Image.objects.all().filter(allowed = user_id)
        serializer = ImageGetSerializer(images, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new image
    def post(self, request, user_id, *args, **kwargs):
        ''' Create the Image '''
        # set Id for image
        count_image = Image.objects.count()
        count_image += 1

        data = {
            'image_id': count_image,
            'image_name': request.data.get('image_name'),  
            'upload_data': datetime.date.today(),
            'allowed': list(user_id)
        }
        
        serializer = ImagePostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Modify "allowed" people for image
    def put(self, request, user_id, *args, **kwargs):
        ''' Updates the image '''
        image_instance = Image.objects.get(Q(image_id = request.data.get('image_id')) & Q(allowed = user_id))

        if not image_instance:
            return Response(
                {"res": "Object with image id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # check for the type
        new_user_id = request.data.get('new_user_id')
        allowed = []

        if isinstance(new_user_id, int):
            allowed.append(new_user_id)
        elif isinstance(new_user_id, str):
            allowed = list(new_user_id)
        elif isinstance(new_user_id, list):
            allowed = new_user_id
        
        data = {
            'image_id': request.data.get('image_id'),
            'allowed': allowed
        }
        
        serializer = ImagePostSerializer(instance = image_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete
    def delete(self, request, user_id, *args, **kwargs):
        ''' Deletes the image '''
        image_to_delete = Image.objects.get(Q(image_id = request.data.get('image_id')) & Q(allowed = user_id))

        if not image_to_delete:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_to_delete.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

# Note API
class NoteView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # Take all image for user
    def get(self, request, user_id, *args, **kwargs):
        ''' List all the note for given requested user '''
        notes = Note.objects.all().filter(allowed = user_id)
        serializer = NoteGetSerializer(notes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new note
    def post(self, request, user_id, *args, **kwargs):
        ''' Create the note '''
        # set Id for image
        count_note = Note.objects.count()
        count_note += 1

        data = {
            'note_id': count_note,
            'title': request.data.get('title'),  
            'body': request.data.get('body'),  
            'create_date': datetime.date.today(),
            'allowed': list(user_id)
        }
        
        serializer = NotePostSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Modify note and people allowed
    def put(self, request, user_id, *args, **kwargs):
        ''' Updates the note '''
        note_instance = Note.objects.get(Q(note_id = request.data.get('note_id')) & Q(allowed = user_id))

        if not note_instance:
            return Response(
                {"res": "Object with image id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # check for the type
        new_user_id = request.data.get('new_user_id')
        allowed = []

        if isinstance(new_user_id, int):
            allowed.append(new_user_id)
        elif isinstance(new_user_id, str):
            allowed = list(new_user_id)
        elif isinstance(new_user_id, list):
            allowed = new_user_id
        
        data = {
            'note_id': request.data.get('note_id'),
            'title': request.data.get('title'),
            'body': request.data.get('body'),
            'allowed': allowed
        }
        
        serializer = NotePostSerializer(instance = note_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete
    def delete(self, request, user_id, *args, **kwargs):
        ''' Deletes the note '''
        note_to_delete = Note.objects.get(Q(note_id = request.data.get('note_id')) & Q(allowed = user_id))

        if not note_to_delete:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        note_to_delete.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

# Calender Api
class CalendarView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # Take all image for user
    def get(self, request, user_id, *args, **kwargs):
        ''' List all the note for given requested user '''
        notes = Calendar.objects.all().filter(allowed = user_id)
        serializer = CalendarGetSerializer(notes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new note
    def post(self, request, user_id, *args, **kwargs):
        ''' Create the note '''
        # set Id for image
        count_note = Calendar.objects.count()
        count_note += 1

        data = {
            'calendar_id': count_note,
            'title': request.data.get('title'),  
            'description': request.data.get('description'),  
            'start_event': request.data.get('start_event'),
            'finish_event': request.data.get('finish_event'),
            'allowed': list(user_id)
        }
        
        serializer = CalendarPostSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Modify note and people allowed
    def put(self, request, user_id, *args, **kwargs):
        ''' Updates the note '''
        calendar_instance = Calendar.objects.get(Q(calendar_id = request.data.get('calendar_id')) & Q(allowed = user_id))

        if not calendar_instance:
            return Response(
                {"res": "Object with image id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # check for the type
        new_user_id = request.data.get('new_user_id')
        allowed = []

        if isinstance(new_user_id, int):
            allowed.append(new_user_id)
        elif isinstance(new_user_id, str):
            allowed = list(new_user_id)
        elif isinstance(new_user_id, list):
            allowed = new_user_id
        
        data = {
            'note_id': request.data.get('note_id'),
            'title': request.data.get('title'),
            'body': request.data.get('body'),
            'allowed': allowed
        }
        
        serializer = NotePostSerializer(instance = calendar_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete
    def delete(self, request, user_id, *args, **kwargs):
        ''' Deletes the note '''
        calendar_to_delete = Calendar.objects.get(Q(calendar_id = request.data.get('calendar_id')) & Q(allowed = user_id))

        if not calendar_to_delete:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        calendar_to_delete.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
