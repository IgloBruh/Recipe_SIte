import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(username='testuser', email='test@example.com', password='testpassword'):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
    return _create_user

@pytest.fixture
def create_recipe(create_user):
    def _create_recipe(title='Test Recipe', author=None):
        if author is None:
            author = create_user()
        
        return Recipe.objects.create(
            title=title,
            ingredients='Test ingredients',
            instructions='Test instructions',
            cooking_time=30,
            difficulty='medium',
            author=author
        )
    return _create_recipe

@pytest.mark.django_db
class TestUserAPI:
    def test_user_registration(self, api_client):
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username='newuser').exists()
    
    def test_user_login(self, api_client, create_user):
        user = create_user()
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

@pytest.mark.django_db
class TestRecipeAPI:
    def test_list_recipes(self, api_client, create_recipe):
        # Создаем несколько рецептов
        create_recipe(title='Recipe 1')
        create_recipe(title='Recipe 2')
        
        url = reverse('recipe-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
    
    def test_create_recipe(self, api_client, create_user):
        user = create_user()
        api_client.force_authenticate(user=user)
        
        url = reverse('recipe-list')
        data = {
            'title': 'New Recipe',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'cooking_time': 45,
            'difficulty': 'easy'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Recipe.objects.filter(title='New Recipe').exists()
    
    def test_retrieve_recipe(self, api_client, create_recipe):
        recipe = create_recipe()
        
        url = reverse('recipe-detail', kwargs={'pk': recipe.id})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Test Recipe'
    
    def test_update_recipe(self, api_client, create_recipe, create_user):
        user = create_user()
        recipe = create_recipe(author=user)
        
        api_client.force_authenticate(user=user)
        url = reverse('recipe-detail', kwargs={'pk': recipe.id})
        data = {
            'title': 'Updated Recipe',
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'cooking_time': recipe.cooking_time,
            'difficulty': recipe.difficulty
        }
        
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        recipe.refresh_from_db()
        assert recipe.title == 'Updated Recipe'
    
    def test_delete_recipe(self, api_client, create_recipe, create_user):
        user = create_user()
        recipe = create_recipe(author=user)
        
        api_client.force_authenticate(user=user)
        url = reverse('recipe-detail', kwargs={'pk': recipe.id})
        
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Recipe.objects.filter(id=recipe.id).exists()
    
    def test_unauthorized_update(self, api_client, create_recipe, create_user):
        # Создаем рецепт от одного пользователя
        author = create_user(username='author')
        recipe = create_recipe(author=author)
        
        # Пытаемся обновить от имени другого пользователя
        other_user = create_user(username='otheruser', email='other@example.com')
        api_client.force_authenticate(user=other_user)
        
        url = reverse('recipe-detail', kwargs={'pk': recipe.id})
        data = {
            'title': 'Unauthorized Update',
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'cooking_time': recipe.cooking_time,
            'difficulty': recipe.difficulty
        }
        
        response = api_client.put(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        
        recipe.refresh_from_db()
        assert recipe.title == 'Test Recipe'  # Название не изменилось

@pytest.mark.django_db
class TestReviewAPI:
    def test_create_review(self, api_client, create_user, create_recipe):
        user = create_user()
        recipe = create_recipe()
        
        api_client.force_authenticate(user=user)
        url = reverse('review-list')
        data = {
            'recipe': recipe.id,
            'rating': 4,
            'comment': 'Great recipe!'
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['rating'] == 4
        assert response.data['comment'] == 'Great recipe!'

@pytest.mark.django_db
class TestFavoriteAPI:
    def test_add_to_favorites(self, api_client, create_user, create_recipe):
        user = create_user()
        recipe = create_recipe()
        
        api_client.force_authenticate(user=user)
        url = reverse('favorite-list')
        data = {
            'recipe': recipe.id
        }
        
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_remove_from_favorites(self, api_client, create_user, create_recipe):
        user = create_user()
        recipe = create_recipe()
        
        # Сначала добавляем в избранное
        api_client.force_authenticate(user=user)
        url = reverse('favorite-list')
        data = {
            'recipe': recipe.id
        }
        response = api_client.post(url, data, format='json')
        favorite_id = response.data['id']
        
        # Затем удаляем из избранного
        url = reverse('favorite-detail', kwargs={'pk': favorite_id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
class TestSearchAndFilter:
    def test_search_recipe(self, api_client, create_recipe):
        create_recipe(title='Pasta Carbonara')
        create_recipe(title='Chicken Soup')
        create_recipe(title='Pasta Bolognese')
        
        url = reverse('recipe-list') + '?search=pasta'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
    
    def test_filter_by_difficulty(self, api_client, create_user):
        user = create_user()
        
        # Создаем рецепты с разной сложностью
        Recipe.objects.create(
            title='Easy Recipe',
            ingredients='Test ingredients',
            instructions='Test instructions',
            cooking_time=15,
            difficulty='easy',
            author=user
        )
        
        Recipe.objects.create(
            title='Medium Recipe',
            ingredients='Test ingredients',
            instructions='Test instructions',
            cooking_time=30,
            difficulty='medium',
            author=user
        )
        
        Recipe.objects.create(
            title='Hard Recipe',
            ingredients='Test ingredients',
            instructions='Test instructions',
            cooking_time=60,
            difficulty='hard',
            author=user
        )
        
        url = reverse('recipe-list') + '?difficulty=easy'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Easy Recipe'
