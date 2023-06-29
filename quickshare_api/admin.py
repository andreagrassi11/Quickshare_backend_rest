from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Image)
admin.site.register(Note)
admin.site.register(Calendar)
admin.site.register(List)
admin.site.register(ListElement)
admin.site.register(Expenses)
admin.site.register(Income)
admin.site.register(Message)