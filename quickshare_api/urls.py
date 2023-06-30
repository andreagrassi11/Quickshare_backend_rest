from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    # User Api
    path('register', RegisterApi.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('user/info/<user_id>', UserInfo.as_view()),
    path('user/info/email/<email>', UserInfoByEmail.as_view()),

    # Image API
    path('image/<user_id>', UserImageView.as_view()),

    # Note API
    path('note/<user_id>', NoteView.as_view(), name='note'),

    # List API
    path('list/<user_id>', ListView.as_view()),
    path('list/element/<list_id>', ListElementView.as_view()),

    # Calendar API
    path('calendar/<user_id>/<date>', CalendarView.as_view()),

    # Finance API
    path('expense/<user_id>', ExpenseView.as_view()),
    path('income/<user_id>', IncomeView.as_view()),
    path('expense/month/<user_id>/<month>', ExpenseMonthView.as_view()),
    path('income/month/<user_id>/<month>', IncomeMonthView.as_view()),

    # Chat API
    path('message/<user_id>', ChatView.as_view()),
]