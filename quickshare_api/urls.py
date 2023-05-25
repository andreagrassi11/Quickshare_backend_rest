from django.urls import path, include
from .views import (
    ImageView,
    ListViewGet,
    ListViewPost
)

urlpatterns = [
    path('image', ImageView.as_view()),
    path('list/?<int:list_id>', ListViewGet.as_view()),
    path('list', ListViewPost.as_view()),
]