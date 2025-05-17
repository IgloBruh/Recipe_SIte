from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Recipe(models.Model):
    """
    Модель рецепта, содержащая всю информацию о блюде.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]
    
    title = models.CharField(max_length=255)
    ingredients = models.TextField()  # Хранение в формате JSON или списком
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text="Время приготовления в минутах")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Дополнительные поля для расширенного функционала
    is_published = models.BooleanField(default=True)
    category = models.CharField(max_length=100, blank=True)
    servings = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
        
    def average_rating(self):
        """Вычисляет среднюю оценку рецепта на основе отзывов."""
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return 0
