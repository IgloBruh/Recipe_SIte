from django.db import models
from django.conf import settings

class Favorite(models.Model):
    """
    Модель для хранения избранных рецептов пользователей.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Один рецепт может быть добавлен в избранное пользователем только один раз
        unique_together = ('user', 'recipe')
        ordering = ['-added_at']
        
    def __str__(self):
        return f"{self.user.username} добавил '{self.recipe.title}' в избранное"
