from django.urls import path, include
from .views import (
    ImageView
)

urlpatterns = [
    path('api', ImageView.as_view()),
]