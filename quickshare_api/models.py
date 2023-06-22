from django.db import models
from django.contrib.auth.models import User

# Image
class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=180)
    upload_data = models.DateField()
    allowed = models.ManyToManyField(User)

# Note
class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 100)
    body = models.TextField()
    create_date = models.DateField()
    allowed = models.ManyToManyField(User)

# Calendar
class Calendar(models.Model):
    calendar_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 100)
    description  = models.TextField()
    start_event = models.DateTimeField()
    finish_event = models.DateTimeField()
    allowed = models.ManyToManyField(User)
    
# List
class List(models.Model):  
    list_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    create_date = models.DateField()
    allowed = models.ManyToManyField(User)

class ListElement(models.Model):  
    list_element_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=130)
    do =  models.BooleanField()
    create_date = models.DateField()
    fk_list = models.ForeignKey(List, on_delete=models.CASCADE, blank=True, null=True)


# Finances
class Expenses(models.Model):
    expenses_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 100)
    category = models.CharField(max_length = 100)
    data = models.DateField()
    amount = models.IntegerField()
    method = models.CharField(max_length = 100)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class Income(models.Model):
    income_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100)
    category = models.CharField(max_length = 100)
    data = models.DateField()
    amount = models.IntegerField()
    method = models.CharField(max_length = 100)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)