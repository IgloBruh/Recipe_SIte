from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm

from favorites.models import Favorite
from reviews.models import Review

User = get_user_model()


class UserProfileView(LoginRequiredMixin, TemplateView):
    """Представление для профиля пользователя"""

    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("pk", self.request.user.id)
        context["user_profile"] = User.objects.get(id=user_id)
        context["user_recipes"] = (
            context["user_profile"].recipes.all().order_by("-created_at")
        )
        context["user_reviews"] = Review.objects.filter(
            user=context["user_profile"]
        ).order_by("-created_at")

        # Избранное показываем только для текущего пользователя
        if user_id == self.request.user.id:
            context["user_favorites"] = Favorite.objects.filter(
                user=self.request.user
            ).order_by("-added_at")

        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля пользователя"""

    model = User
    template_name = "users/edit_profile.html"
    fields = ["username", "email", "bio", "profile_picture"]
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Ошибка при обновлении профиля. Пожалуйста, проверьте введенные данные.",
        )
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    """Кастомное представление для входа в систему"""

    template_name = "users/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, f"Добро пожаловать, {form.get_user().username}!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Ошибка входа. Пожалуйста, проверьте имя пользователя и пароль.",
        )
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """Кастомное представление для выхода из системы"""

    next_page = reverse_lazy("home")  # Перенаправление на главную страницу после выхода

    # Разрешаем как GET, так и POST запросы
    http_method_names = ["get", "post"]

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Вы успешно вышли из системы.")
        return super().dispatch(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    """Представление для регистрации пользователей"""
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Автоматический вход после регистрации
        login(self.request, self.object)
        messages.success(self.request, f'Аккаунт успешно создан! Добро пожаловать, {self.object.username}!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при регистрации. Пожалуйста, проверьте введенные данные.')
        return super().form_invalid(form)
