from django.contrib import admin
from django.urls import path, include
from quickshare_api import urls as quickshare_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('quickshare/', include(quickshare_urls)),
]
