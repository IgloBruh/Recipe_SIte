# Проектирование моделей данных для платформы обмена рецептами

## Модель User
Расширяет стандартную модель пользователя Django для аутентификации и авторизации.

```python
class User(AbstractUser):
    """
    Модель пользователя с расширенными полями для платформы рецептов.
    Наследуется от AbstractUser Django для использования встроенной системы аутентификации.
    """
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    # Дополнительные поля для JWT
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
```

## Модель Recipe
Основная модель для хранения информации о рецептах.

```python
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
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='recipes')
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
```

## Модель Review
Модель для хранения отзывов и оценок пользователей о рецептах.

```python
class Review(models.Model):
    """
    Модель отзыва пользователя о рецепте с оценкой.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reviews')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='reviews')
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
```

## Модель Favorite
Модель для хранения избранных рецептов пользователей.

```python
class Favorite(models.Model):
    """
    Модель для хранения избранных рецептов пользователей.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Один рецепт может быть добавлен в избранное пользователем только один раз
        unique_together = ('user', 'recipe')
        ordering = ['-added_at']
        
    def __str__(self):
        return f"{self.user.username} добавил '{self.recipe.title}' в избранное"
```

## Связи между моделями

1. **User и Recipe**:
   - Один пользователь может создать множество рецептов (One-to-Many)
   - Связь через ForeignKey в модели Recipe (поле author)

2. **User и Review**:
   - Один пользователь может оставить множество отзывов (One-to-Many)
   - Связь через ForeignKey в модели Review (поле user)

3. **Recipe и Review**:
   - Один рецепт может иметь множество отзывов (One-to-Many)
   - Связь через ForeignKey в модели Review (поле recipe)

4. **User и Favorite**:
   - Один пользователь может добавить множество рецептов в избранное (One-to-Many)
   - Связь через ForeignKey в модели Favorite (поле user)

5. **Recipe и Favorite**:
   - Один рецепт может быть добавлен в избранное множеством пользователей (One-to-Many)
   - Связь через ForeignKey в модели Favorite (поле recipe)

## Дополнительные соображения

1. **Индексы**:
   - Поля, используемые для поиска и фильтрации (title, ingredients, cooking_time, difficulty), должны быть проиндексированы
   - Поля внешних ключей (ForeignKey) автоматически индексируются Django

2. **Валидация**:
   - Для рейтинга используются валидаторы Django (MinValueValidator, MaxValueValidator)
   - Для уникальных комбинаций полей используется unique_together

3. **Расширяемость**:
   - Модель Recipe включает дополнительные поля (is_published, category, servings) для будущего расширения функционала
   - Модель User расширяет AbstractUser для возможности добавления дополнительных полей

4. **Безопасность**:
   - Используется каскадное удаление (on_delete=models.CASCADE) для поддержания целостности данных
   - Для хранения паролей используется встроенная система хеширования Django
