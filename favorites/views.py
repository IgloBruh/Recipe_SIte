from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Favorite
from .serializers import FavoriteSerializer
from recipes.permissions import IsAuthorOrReadOnly

class FavoriteViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с избранными рецептами.
    Обеспечивает CRUD-операции для избранного.
    Поддерживает фильтрацию и пагинацию.
    """
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['recipe']
    ordering_fields = ['added_at']
    ordering = ['-added_at']
    
    def get_queryset(self):
        """Возвращает избранные рецепты текущего пользователя"""
        return Favorite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Сохраняет текущего пользователя как владельца избранного"""
        serializer.save(user=self.request.user)
