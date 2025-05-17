from django_filters import rest_framework as filters
from .models import Recipe

class RecipeFilter(filters.FilterSet):
    """
    Фильтр для рецептов, позволяющий фильтровать по различным параметрам.
    """
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    ingredients = filters.CharFilter(field_name='ingredients', lookup_expr='icontains')
    min_cooking_time = filters.NumberFilter(field_name='cooking_time', lookup_expr='gte')
    max_cooking_time = filters.NumberFilter(field_name='cooking_time', lookup_expr='lte')
    difficulty = filters.ChoiceFilter(choices=Recipe.DIFFICULTY_CHOICES)
    category = filters.CharFilter(field_name='category', lookup_expr='icontains')
    author = filters.NumberFilter(field_name='author__id')
    
    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'difficulty', 'category', 'author']
