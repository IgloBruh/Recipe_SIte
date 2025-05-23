# Проект "Платформа обмена рецептами"

## Обзор проекта

Разработана полноценная веб-платформа для обмена рецептами с использованием Django и Django REST Framework. Платформа предоставляет пользователям возможность регистрации, создания и публикации рецептов, оценки и комментирования рецептов других пользователей, а также добавления рецептов в избранное.

## Реализованный функционал

### Бэкенд

1. **Аутентификация и авторизация**
   - Реализована JWT-аутентификация
   - Регистрация новых пользователей
   - Вход и выход из системы
   - Защита эндпоинтов с помощью разрешений

2. **Модели данных**
   - User (id, username, email, password_hash, registration_date)
   - Recipe (id, title, ingredients, instructions, cooking_time, difficulty, author_id, created_at, updated_at)
   - Review (id, user_id, recipe_id, rating, comment, created_at)
   - Favorite (user_id, recipe_id)

3. **RESTful API**
   - CRUD операции для всех моделей
   - Поиск и фильтрация рецептов (по названию, ингредиентам, времени приготовления, сложности)
   - Пагинация результатов
   - Валидация входных данных
   - Документация API (Swagger/OpenAPI)

4. **Дополнительные функции**
   - Обработка ошибок
   - Логирование
   - Загрузка и обработка изображений
   - Автоматические тесты для основных эндпоинтов

### Фронтенд

1. **Страницы**
   - Главная страница с популярными рецептами
   - Страница деталей рецепта
   - Личный кабинет пользователя
   - Формы создания/редактирования рецептов
   - Страницы входа и регистрации

2. **Функциональность**
   - Адаптивный дизайн (Bootstrap)
   - Загрузка изображений для рецептов
   - Система оценок и отзывов (1-5 звёзд)
   - Добавление/удаление рецептов в избранное
   - Поиск и фильтрация рецептов

## Технические детали

1. **Используемые технологии**
   - Backend: Django, Django REST Framework, JWT
   - Frontend: HTML, CSS, JavaScript, Bootstrap
   - База данных: SQLite
   - Документация: Swagger/OpenAPI

2. **Структура проекта**
   - Модульная архитектура с разделением на приложения
   - Следование принципам MVT (Model-View-Template)
   - Разделение бэкенд и фронтенд логики

3. **Безопасность**
   - Защита от CSRF
   - Валидация входных данных
   - Проверка прав доступа
   - Безопасное хранение паролей

## Инструкция по запуску

1. **Установка зависимостей**
   ```
   pip install -r requirements.txt
   ```

2. **Настройка базы данных**
   ```
   python manage.py migrate
   ```

3. **Создание суперпользователя (опционально)**
   ```
   python manage.py createsuperuser
   ```

4. **Запуск сервера**
   ```
   python manage.py runserver
   ```

5. **Доступ к API документации**
   - Swagger UI: http://localhost:8000/swagger/
   - ReDoc: http://localhost:8000/redoc/

## Руководство по использованию API

### 1. Получение JWT-токена (аутентификация)

Сначала необходимо получить JWT-токен для аутентификации:

```
POST http://127.0.0.1:8000/api/users/token/
Content-Type: application/json

{
    "username": "ваш_логин",
    "password": "ваш_пароль"
}
```

В ответ вы получите:
```json
{
    "refresh": "refresh_token_value",
    "access": "access_token_value"
}
```

Сохраните `access_token_value` - он понадобится для всех последующих запросов.

### 2. Основные эндпоинты API

#### Рецепты

- **Получение списка рецептов**:
  ```
  GET http://127.0.0.1:8000/api/recipes/
  Authorization: Bearer access_token_value
  ```

- **Получение конкретного рецепта**:
  ```
  GET http://127.0.0.1:8000/api/recipes/1/
  Authorization: Bearer access_token_value
  ```

- **Создание нового рецепта**:
  ```
  POST http://127.0.0.1:8000/api/recipes/
  Content-Type: application/json
  Authorization: Bearer access_token_value
  
  {
      "title": "Название рецепта",
      "ingredients": "Список ингредиентов",
      "instructions": "Инструкции по приготовлению",
      "cooking_time": 30,
      "difficulty": "medium"
  }
  ```

- **Обновление рецепта**:
  ```
  PUT http://127.0.0.1:8000/api/recipes/1/
  Content-Type: application/json
  Authorization: Bearer access_token_value
  
  {
      "title": "Новое название",
      "ingredients": "Обновленные ингредиенты",
      "instructions": "Обновленные инструкции",
      "cooking_time": 45,
      "difficulty": "hard"
  }
  ```

- **Удаление рецепта**:
  ```
  DELETE http://127.0.0.1:8000/api/recipes/1/
  Authorization: Bearer access_token_value
  ```

#### Отзывы

- **Получение отзывов**:
  ```
  GET http://127.0.0.1:8000/api/reviews/
  Authorization: Bearer access_token_value
  ```

- **Добавление отзыва**:
  ```
  POST http://127.0.0.1:8000/api/reviews/
  Content-Type: application/json
  Authorization: Bearer access_token_value
  
  {
      "recipe": 1,
      "rating": 5,
      "comment": "Отличный рецепт!"
  }
  ```

#### Избранное

- **Получение избранных рецептов**:
  ```
  GET http://127.0.0.1:8000/api/favorites/
  Authorization: Bearer access_token_value
  ```

- **Добавление в избранное**:
  ```
  POST http://127.0.0.1:8000/api/favorites/
  Content-Type: application/json
  Authorization: Bearer access_token_value
  
  {
      "recipe": 1
  }
  ```

- **Удаление из избранного**:
  ```
  DELETE http://127.0.0.1:8000/api/favorites/1/
  Authorization: Bearer access_token_value
  ```

### 3. Поиск и фильтрация

Вы можете использовать параметры запроса для поиска и фильтрации:

- **Поиск по названию**:
  ```
  GET http://127.0.0.1:8000/api/recipes/?search=паста
  ```

- **Фильтрация по сложности**:
  ```
  GET http://127.0.0.1:8000/api/recipes/?difficulty=easy
  ```

- **Фильтрация по времени приготовления**:
  ```
  GET http://127.0.0.1:8000/api/recipes/?min_cooking_time=10&max_cooking_time=30
  ```

### 4. Пагинация

API поддерживает пагинацию. По умолчанию возвращается 10 результатов на страницу:

```
GET http://127.0.0.1:8000/api/recipes/?page=2
```

## Возможности для дальнейшего развития

1. Добавление более сложной рекомендательной системы
2. Интеграция с социальными сетями
3. Добавление функции поиска по нутриентам
4. Реализация мобильного приложения
5. Переход на PostgreSQL для продакшн-окружения
6. Добавление системы уведомлений
7. Расширение функциональности профиля пользователя

