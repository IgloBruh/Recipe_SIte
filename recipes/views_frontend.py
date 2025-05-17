from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Avg, Count

from recipes.models import Recipe
from reviews.models import Review
from favorites.models import Favorite

class HomeView(TemplateView):
    """Представление для главной страницы"""
    template_name = 'recipes/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем популярные рецепты (с наибольшим количеством отзывов и высоким рейтингом)
        context['popular_recipes'] = Recipe.objects.annotate(
            review_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')
        ).filter(is_published=True).order_by('-review_count', '-avg_rating')[:6]
        
        # Получаем новые рецепты
        context['new_recipes'] = Recipe.objects.filter(is_published=True).order_by('-created_at')[:8]
        
        return context

class RecipeListView(ListView):
    """Представление для списка рецептов"""
    model = Recipe
    template_name = 'recipes/list.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Recipe.objects.filter(is_published=True).order_by('-created_at')
        
        # Применяем фильтры из GET-параметров
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search)
            
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
            
        min_time = self.request.GET.get('min_time')
        if min_time:
            queryset = queryset.filter(cooking_time__gte=min_time)
            
        max_time = self.request.GET.get('max_time')
        if max_time:
            queryset = queryset.filter(cooking_time__lte=max_time)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Recipe.objects.values('category').distinct()
        return context

class RecipeDetailView(DetailView):
    """Представление для детальной страницы рецепта"""
    model = Recipe
    template_name = 'recipes/detail.html'
    context_object_name = 'recipe'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        
        # Проверяем, добавлен ли рецепт в избранное текущим пользователем
        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(
                user=self.request.user, 
                recipe=recipe
            ).exists()
            
            # Проверяем, оставил ли пользователь отзыв
            context['user_has_review'] = Review.objects.filter(
                user=self.request.user,
                recipe=recipe
            ).exists()
        
        # Получаем похожие рецепты (той же категории или того же автора)
        similar_recipes = Recipe.objects.filter(
            is_published=True
        ).exclude(id=recipe.id)
        
        if recipe.category:
            category_recipes = similar_recipes.filter(category=recipe.category)
            author_recipes = similar_recipes.filter(author=recipe.author)
            
            # Объединяем и ограничиваем количество
            context['similar_recipes'] = (category_recipes | author_recipes).distinct()[:5]
        else:
            context['similar_recipes'] = similar_recipes.filter(author=recipe.author)[:5]
        
        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания рецепта"""
    model = Recipe
    template_name = 'recipes/create.html'
    fields = ['title', 'category', 'ingredients', 'instructions', 'cooking_time', 
              'difficulty', 'servings', 'image', 'is_published']
    success_url = reverse_lazy('recipe_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Рецепт успешно создан!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании рецепта. Пожалуйста, проверьте введенные данные.')
        return super().form_invalid(form)

class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования рецепта"""
    model = Recipe
    template_name = 'recipes/edit.html'
    fields = ['title', 'category', 'ingredients', 'instructions', 'cooking_time', 
              'difficulty', 'servings', 'image', 'is_published']
    
    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        # Проверяем, является ли текущий пользователь автором рецепта
        obj = self.get_object()
        if obj.author != self.request.user:
            messages.error(request, 'У вас нет прав для редактирования этого рецепта.')
            return redirect('recipe_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Рецепт успешно обновлен!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при обновлении рецепта. Пожалуйста, проверьте введенные данные.')
        return super().form_invalid(form)
