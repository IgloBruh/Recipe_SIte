from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe
from .serializers import RecipeSerializer, RecipeDetailSerializer
from .permissions import IsAuthorOrReadOnly
from .filters import RecipeFilter

class RecipeViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с рецептами.
    Обеспечивает CRUD-операции для рецептов.
    Поддерживает поиск, фильтрацию и пагинацию.
    """
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RecipeFilter
    search_fields = ['title', 'ingredients', 'category']
    ordering_fields = ['created_at', 'cooking_time', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Возвращает разные сериализаторы в зависимости от действия"""
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer):
        """Сохраняет текущего пользователя как автора рецепта"""
        serializer.save(author=self.request.user)
