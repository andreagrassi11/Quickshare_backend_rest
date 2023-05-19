from django.contrib import admin
from .models import Image, List, ListElement

# Register your models here.
admin.site.register(Image)
admin.site.register(List)
admin.site.register(ListElement)