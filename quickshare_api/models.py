from django.db import models
from django.contrib.auth.models import User

# User
# class User(models.Model):
#     user_id = models.IntegerField(primary_key = True)
#     name = models.CharField(max_length=50)
#     surname = models.CharField(max_length=50)
#     email = models.EmailField(max_length=254)
#     password = models.CharField(max_length=50) # hash
#     date_joined = models.DateField()
#     reset_password = models.BooleanField()

# Image
class Image(models.Model):
    image_id = models.IntegerField(primary_key = True)
    image_name = models.CharField(max_length=180)
    upload_data = models.DateField()
    allowed = models.ManyToManyField(User)

# Note
class Note(models.Model):
    note_id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length = 100)
    body = models.TextField()
    create_date = models.DateField()
    allowed = models.ManyToManyField(User)

# Calendar
class Calendar(models.Model):
    calendar_id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length = 100)
    description  = models.TextField()
    start_event = models.DateTimeField()
    finish_event = models.DateTimeField()
    allowed = models.ManyToManyField(User)
    
# List
class List(models.Model):  
    list_id = models.IntegerField(primary_key = True)
    title = models.CharField(max_length=50)
    descrizione = models.CharField(max_length=150)
    create_data = models.DateField()
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class ListElement(models.Model):  
    list_element_id = models.IntegerField(primary_key = True)
    description = models.CharField(max_length=130)
    do =  models.BooleanField()
    fk_list = models.ForeignKey(List, on_delete=models.CASCADE, blank=True, null=True)

class CanAccessList(models.Model):
    id = models.IntegerField(primary_key = True)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    fk_list = models.ForeignKey(List, on_delete=models.CASCADE, blank=True, null=True)
    autorized_data = models.DateField()

# Finances
class FinancialTracker(models.Model):
    financial_id = models.IntegerField(primary_key = True)
    create_date = models.DateField()
    income_sum = models.IntegerField()
    expenses_sum = models.IntegerField()

class CanAccessFinancialTracker(models.Model):
    id = models.IntegerField(primary_key = True)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    fk_financial = models.ForeignKey(FinancialTracker, on_delete=models.CASCADE, blank=True, null=True)
    autorized_data = models.DateField()

class Expenses(models.Model):
    expenses_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    category = models.CharField(max_length = 100)
    data = models.DateField()
    amount = models.IntegerField()
    method = models.CharField(max_length = 100)
    comment = models.TextField()
    fk_financial = models.ForeignKey(FinancialTracker, on_delete=models.CASCADE, blank=True, null=True)

class Income(models.Model):
    income_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 100)
    category = models.CharField(max_length = 100)
    data = models.DateField()
    amount = models.IntegerField()
    method = models.CharField(max_length = 100)
    comment = models.TextField()
    fk_financial = models.ForeignKey(FinancialTracker, on_delete=models.CASCADE, blank=True, null=True)