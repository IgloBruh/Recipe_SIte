from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserDetailView

urlpatterns = [
    # JWT аутентификация
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Регистрация и профиль пользователя
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserDetailView.as_view(), name='profile'),
]
