import logging
from django.conf import settings

# Настройка логирования
logger = logging.getLogger(__name__)

class LoggingMiddleware:
    """
    Middleware для логирования запросов и ответов.
    Записывает информацию о входящих запросах и исходящих ответах.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Логирование запроса
        self.log_request(request)
        
        # Получение ответа
        response = self.get_response(request)
        
        # Логирование ответа
        self.log_response(request, response)
        
        return response
    
    def log_request(self, request):
        """Логирует информацию о входящем запросе"""
        user_info = "Анонимный пользователь"
        if request.user.is_authenticated:
            user_info = f"Пользователь: {request.user.username} (ID: {request.user.id})"
        
        logger.info(
            f"Запрос: {request.method} {request.path} | "
            f"{user_info} | "
            f"IP: {self.get_client_ip(request)}"
        )
        
        # Логирование параметров запроса (только в режиме отладки)
        if settings.DEBUG:
            if request.method in ['POST', 'PUT', 'PATCH']:
                logger.debug(f"Данные запроса: {request.POST}")
            elif request.method == 'GET':
                logger.debug(f"Параметры запроса: {request.GET}")
    
    def log_response(self, request, response):
        """Логирует информацию об исходящем ответе"""
        logger.info(
            f"Ответ: {request.method} {request.path} | "
            f"Статус: {response.status_code} | "
            f"Размер: {len(response.content) if hasattr(response, 'content') else 'N/A'} байт"
        )
        
        # Логирование ошибок
        if 400 <= response.status_code < 500:
            logger.warning(
                f"Клиентская ошибка: {request.method} {request.path} | "
                f"Статус: {response.status_code}"
            )
        elif response.status_code >= 500:
            logger.error(
                f"Серверная ошибка: {request.method} {request.path} | "
                f"Статус: {response.status_code}"
            )
    
    def get_client_ip(self, request):
        """Получает IP-адрес клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class APIExceptionMiddleware:
    """
    Middleware для обработки исключений в API.
    Обеспечивает единообразный формат ответов при ошибках.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        """Обрабатывает исключения и возвращает соответствующий ответ"""
        # Проверяем, является ли запрос API-запросом
        if request.path.startswith('/api/'):
            # Логируем исключение
            logger.error(
                f"Исключение в API: {request.method} {request.path} | "
                f"Тип: {type(exception).__name__} | "
                f"Сообщение: {str(exception)}",
                exc_info=True
            )
            
            # Здесь можно добавить обработку различных типов исключений
            # и возвращать соответствующие HTTP-ответы
            
            # Пример: можно вернуть JSON-ответ с информацией об ошибке
            # from django.http import JsonResponse
            # return JsonResponse({
            #     'error': type(exception).__name__,
            #     'message': str(exception)
            # }, status=500)
            
            # По умолчанию позволяем Django обработать исключение
            return None
