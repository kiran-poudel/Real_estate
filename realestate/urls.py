
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenVerifyView

urlpatterns = [
    path('api/token/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view()),
    path('api/token/verify/',TokenVerifyView.as_view()),
    path('auth/user/',include('users.urls')),
    path('api/property/',include('properties.urls')),
    path('payment/',include('payments.urls')),
    path('admin/', admin.site.urls),
]
