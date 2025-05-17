from rest_framework import serializers
from .models import Recipe
from reviews.models import Review

class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецепта"""
    author_username = serializers.ReadOnlyField(source='author.username')
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Recipe
        fields = (
            'id', 'title', 'ingredients', 'instructions', 'cooking_time', 
            'difficulty', 'image', 'author', 'author_username', 'created_at', 
            'updated_at', 'is_published', 'category', 'servings', 'average_rating'
        )
        read_only_fields = ('id', 'author', 'author_username', 'created_at', 'updated_at', 'average_rating')
    
    def get_average_rating(self, obj):
        """Получает среднюю оценку рецепта"""
        return obj.average_rating()
    
    def create(self, validated_data):
        """Создает новый рецепт с текущим пользователем в качестве автора"""
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class RecipeDetailSerializer(RecipeSerializer):
    """Расширенный сериализатор для детального представления рецепта"""
    reviews = serializers.SerializerMethodField()
    
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('reviews',)
    
    def get_reviews(self, obj):
        """Получает отзывы для рецепта"""
        from reviews.serializers import ReviewSerializer
        reviews = obj.reviews.all()
        return ReviewSerializer(reviews, many=True).data
