from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Расширенная модель пользователя"""
    bio = models.TextField(blank=True, verbose_name="О себе")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Фото профиля")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
