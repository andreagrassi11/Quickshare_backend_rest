from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    id = models.IntegerField(primary_key = True)
    image_name = models.CharField(max_length=180)
    upload_data = models.DateField()
