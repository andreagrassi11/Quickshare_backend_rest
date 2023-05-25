from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Image)
admin.site.register(CanAccessImage)
admin.site.register(List)
admin.site.register(ListElement)
admin.site.register(CanAccessList)
admin.site.register(Note)
admin.site.register(CanAccessNote)
admin.site.register(FinancialTracker)
admin.site.register(CanAccessFinancialTracker)
admin.site.register(Expenses)
admin.site.register(Income)
