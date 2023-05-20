from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    image_id = models.IntegerField(primary_key = True)
    image_name = models.CharField(max_length=180)
    upload_data = models.DateField()

# class List(models.Model):  
#     id = models.IntegerField(primary_key = True)
#     title = models.CharField(max_length=50)
#     descrizione = title = models.CharField(max_length=150)
#     create_data = models.DateField()

# class ListElement(models.Model):  
#     id = models.IntegerField(primary_key = True)
#     description = models.CharField(max_length=130)
#     do =  models.BooleanField()
#     fk_list = models.ForeignKey(List, on_delete=models.CASCADE)
