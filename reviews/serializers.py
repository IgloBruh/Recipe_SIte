from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзыва"""
    user_username = serializers.ReadOnlyField(source='user.username')
    recipe_title = serializers.ReadOnlyField(source='recipe.title')
    
    class Meta:
        model = Review
        fields = ('id', 'user', 'user_username', 'recipe', 'recipe_title', 'rating', 'comment', 'created_at')
        read_only_fields = ('id', 'user', 'user_username', 'recipe_title', 'created_at')
    
    def create(self, validated_data):
        """Создает новый отзыв с текущим пользователем"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
