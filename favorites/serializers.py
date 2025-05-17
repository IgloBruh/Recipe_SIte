from rest_framework import serializers
from .models import Favorite

class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели избранного"""
    user_username = serializers.ReadOnlyField(source='user.username')
    recipe_title = serializers.ReadOnlyField(source='recipe.title')
    
    class Meta:
        model = Favorite
        fields = ('id', 'user', 'user_username', 'recipe', 'recipe_title', 'added_at')
        read_only_fields = ('id', 'user', 'user_username', 'recipe_title', 'added_at')
    
    def create(self, validated_data):
        """Создает новую запись избранного с текущим пользователем"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
