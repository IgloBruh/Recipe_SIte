from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer
from recipes.permissions import IsAuthorOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с отзывами.
    Обеспечивает CRUD-операции для отзывов.
    Поддерживает фильтрацию, поиск и пагинацию.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['recipe', 'user', 'rating']
    search_fields = ['comment']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        """Сохраняет текущего пользователя как автора отзыва"""
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        """
        Опционально фильтрует отзывы по рецепту, если указан параметр recipe_id
        """
        queryset = Review.objects.all()
        recipe_id = self.request.query_params.get('recipe_id', None)
        if recipe_id is not None:
            queryset = queryset.filter(recipe_id=recipe_id)
        return queryset
