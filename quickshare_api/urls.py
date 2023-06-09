from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    # User Api
    path('register', RegisterApi.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/info/<user_id>', UserInfo.as_view()),
    path('user/info/email/', UserInfoByEmail.as_view()),
    # Image API
    path('image/<user_id>', UserImageView.as_view()),
    # Note API
    path('note/<user_id>', NoteView.as_view()),
]