from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from recipes.views_frontend import HomeView, RecipeListView, RecipeDetailView, RecipeCreateView, RecipeUpdateView
from users.views_frontend import UserProfileView, UserUpdateView, CustomLoginView, CustomLogoutView, UserRegistrationView
from .swagger import urlpatterns as swagger_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/favorites/', include('favorites.urls')),
    
    # Frontend routes
    path('', HomeView.as_view(), name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_edit'),
    
    # User routes
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', UserUpdateView.as_view(), name='profile_edit'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
]

# Swagger documentation
urlpatterns += swagger_urls

# Media and static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
