from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    """
    Модель отзыва пользователя о рецепте с оценкой.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Оценка от 1 до 5"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Один пользователь может оставить только один отзыв на рецепт
        unique_together = ('user', 'recipe')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Отзыв от {self.user.username} на рецепт '{self.recipe.title}'"
