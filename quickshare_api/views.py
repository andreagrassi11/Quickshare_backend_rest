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
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from Levenshtein import ratio

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

class UserInfo(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all user information
    def get(self, request, user_id, *args, **kwargs):
        ''' List all the image for given requested user '''
        users = User.objects.all().filter(id = user_id)
        serializer = UserGetSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserInfoByEmail(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all user information
    def get(self, request, email, *args, **kwargs):
        ''' List all the image for given requested user '''
        users = User.objects.all().filter(email = email)
        serializer = UserGetSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Image API    
class UserImageView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all image for user
    def get(self, request, user_id, *args, **kwargs):
        ''' List all the image for given requested user '''
        images = Image.objects.all().filter(allowed = user_id)
        serializer = ImageGetSerializer(images, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new image
    def post(self, request, user_id, *args, **kwargs):

        data = {
            'data': request.data.get('data'),  
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
                {"res": "Object with iamges id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image_to_delete.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
    # Remove share user
    # def patch(self, request, user_id, *args, **kwargs):

# Note API
class NoteView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all image for user
    def get(self, request, user_id, *args, **kwargs):
        ''' List all the note for given requested user '''
        notes = Note.objects.all().filter(allowed = user_id).order_by('-create_date')
        serializer = NoteGetSerializer(notes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new note
    def post(self, request, user_id, *args, **kwargs):
        ''' Create the note '''
        data = {
            'title': request.data.get('title'),  
            'body': request.data.get('body'),  
            'create_date': datetime.date.today(),
            'allowed': [user_id]
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
    def get(self, request, user_id, date, *args, **kwargs):
        
        notes = Calendar.objects.all().filter(Q(fk_user = user_id) & Q(date = date)).order_by('-date')
        serializer = CalendarSerializer(notes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new note
    def post(self, request, user_id, date, *args, **kwargs):
    
        data = {
            'title': request.data.get('title'),  
            'date': date,  
            'fk_user': user_id,
        }
        
        serializer = CalendarSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete
    def delete(self, request, user_id, date, *args, **kwargs):
        
        calendar_to_delete = Calendar.objects.get(Q(calendar_id = date) & Q(fk_user = user_id))

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

# List API
class ListView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all lists for user
    def get(self, request, user_id, *args, **kwargs):
        ''' List all the list for given requested user '''
        lists = List.objects.all().filter(allowed = user_id).order_by('-create_date')
        serializer = ListGetSerializer(lists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new list
    def post(self, request, user_id, *args, **kwargs):
        ''' Create the list '''
        data = {
            'title': request.data.get('title'),  
            'create_date': datetime.date.today(),
            'allowed': [user_id]
        }
        
        serializer = ListPostSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Modify list and people allowed
    def put(self, request, user_id, *args, **kwargs):
        ''' Updates the note '''
        list_instance = List.objects.get(Q(list_id = request.data.get('list_id')) & Q(allowed = user_id))

        if not list_instance:
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
            'title': request.data.get('title'),
            'allowed': allowed
        }
        
        serializer = ListPostSerializer(instance = list_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete list
    def delete(self, request, user_id, *args, **kwargs):
        ''' Deletes the note '''
        note_to_delete = List.objects.get(Q(list_id = request.data.get('list_id')) & Q(allowed = user_id))

        if not note_to_delete:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        
        note_to_delete.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class ListElementView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all list element for list
    def get(self, request, list_id, *args, **kwargs):

        list_element = ListElement.objects.all().filter(fk_list = list_id).order_by('-create_date')
        serializer = ListElementSerializer(list_element, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new list element
    def post(self, request, list_id, *args, **kwargs):
        
        data = {
            'description': request.data.get('description'), 
            'do': False,
            'create_date': datetime.date.today(),
            'fk_list': list_id
        }
        
        serializer = ListElementSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Modify list element
    def put(self, request, list_id, *args, **kwargs):
        
        list_element_instance = ListElement.objects.filter(list_element_id = request.data.get('list_element_id')).first()

        if not list_element_instance:
            return Response(
                {"res": "Object with image id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'do': request.data.get('do')
        }
        
        serializer = ListElementPutSerializer(instance = list_element_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete
    def delete(self, request, list_id, *args, **kwargs):
        
        list_element_to_delete = ListElement.objects.filter(list_element_id = request.data.get('list_element_id')).first()

        if not list_element_to_delete:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        
        list_element_to_delete.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

# Finances
class ExpenseView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all expenses for user
    def get(self, request, user_id, *args, **kwargs):
        
        lists = Expenses.objects.all().filter(fk_user = user_id).order_by('-data')
        serializer = ExpenseSerializer(lists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new list
    def post(self, request, user_id, *args, **kwargs):
        ''' Create the list '''
        data = {
            'title': request.data.get('title'), 
            'category': request.data.get('category'), 
            'data': request.data.get('data'), 
            'amount': request.data.get('amount'), 
            'method': request.data.get('method'), 
            'fk_user': user_id, 
        }
        
        serializer = ExpenseSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete list
    def delete(self, request, user_id, *args, **kwargs):
        ''' Deletes the note '''
        expenses_to_delete = Expenses.objects.all().filter(fk_user = user_id).first()

        if not expenses_to_delete:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        
        expenses_to_delete.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
    
class IncomeView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all expenses for user
    def get(self, request, user_id, *args, **kwargs):
        
        lists = Income.objects.all().filter(fk_user = user_id).order_by('-data')
        serializer = IncomeSerializer(lists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new list
    def post(self, request, user_id, *args, **kwargs):
        ''' Create the list '''
        data = {
            'name': request.data.get('name'), 
            'category': request.data.get('category'), 
            'data': request.data.get('data'), 
            'amount': request.data.get('amount'), 
            'method': request.data.get('method'), 
            'fk_user': user_id, 
        }
        
        serializer = IncomeSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete list
    def delete(self, request, user_id, *args, **kwargs):
        ''' Deletes the note '''
        income_to_delete = Income.objects.all().filter(fk_user = user_id).first()

        if not income_to_delete:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
        
        income_to_delete.delete()

        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class ExpenseMonthView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all expenses for user
    def get(self, request, user_id, month, *args, **kwargs):
        
        lists = Expenses.objects.all().filter(Q(fk_user = user_id) & Q(data__month = month)).order_by('-data')
        serializer = ExpenseSerializer(lists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class IncomeMonthView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all expenses for user
    def get(self, request, user_id, month, *args, **kwargs):
        
        lists = Income.objects.all().filter(Q(fk_user = user_id) & Q(data__month = month)).order_by('-data')
        serializer = IncomeSerializer(lists, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# Chat
class ChatView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    # Take all message for user
    def get(self, request, user_id, *args, **kwargs):
        
        messages = Message.objects.all().filter(allowed = user_id).order_by('-date')
        serializer = ChatSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # Insert a new message
    def post(self, request, user_id, *args, **kwargs):
        
        data = {
            'message': request.data.get('message'), 
            'date': datetime.date.today(), 
            'fk_user_creator': user_id, 
            'allowed': list(user_id), 
        }
        
        serializer = ChatSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Modify people allowed
    def put(self, request, user_id, *args, **kwargs):

        message_instance = Message.objects.get(Q(message_id = request.data.get('message_id')) & Q(allowed = user_id))

        if not message_instance:
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
            'allowed': allowed
        }
        
        serializer = ChatPutSerializer(instance = message_instance, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchNotesView(APIView):
    # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id, text, *args, **kwargs):
    
        note_objects = Note.objects.all().filter(allowed=user_id)

        serializer = SearchNotesGetSerializer(note_objects, many=True)

        note_objects_list = []
        note_objects_filtered = []

        for key in serializer.data:
            note_objects_list.append(dict(key))

        for index in range(len(note_objects_list)):
            if ratio(note_objects_list[index]['title'], text) >= 0.6:
                note_objects_filtered.append(note_objects_list[index])

        return Response(note_objects_filtered, status=status.HTTP_200_OK)
    

class SearchListsView(APIView):
     # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id, text, *args, **kwargs):
    
        list_objects = List.objects.all().filter(allowed=user_id)

        serializer = SearchListsGetSerializer(list_objects, many=True)

        list_objects_list = []
        list_objects_filtered = []

        for key in serializer.data:
            list_objects_list.append(dict(key))

        for index in range(len(list_objects_list)):
            if ratio(list_objects_list[index]['title'], text) >= 0.6:
                list_objects_filtered.append(list_objects_list[index])

        return Response(list_objects_filtered, status=status.HTTP_200_OK)


class SearchEventsView(APIView):
     # add permission to check if user is authenticated
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id, text, *args, **kwargs):
    
        event_objects = Calendar.objects.all().filter(fk_user=user_id)

        serializer = SearchCalendarGetSerializer(event_objects, many=True)

        event_objects_list = []
        event_objects_filtered = []

        for key in serializer.data:
            event_objects_list.append(dict(key))

        for index in range(len(event_objects_list)):
            if ratio(event_objects_list[index]['title'], text) >= 0.6:
                event_objects_filtered.append(event_objects_list[index])

        return Response(event_objects_filtered, status=status.HTTP_200_OK)
