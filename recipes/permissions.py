from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Пользовательское разрешение, позволяющее только авторам объекта редактировать его.
    """
    
    def has_object_permission(self, request, view, obj):
        # Разрешения на чтение разрешены для любого запроса
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Разрешения на запись разрешены только автору объекта
        return obj.author == request.user
