import os
import logging
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

# Настройка логирования
logger = logging.getLogger(__name__)

def validate_image_file(image):
    """
    Валидирует загруженное изображение.
    Проверяет формат, размер и другие параметры.
    """
    try:
        # Проверка размера файла (максимум 5MB)
        if image.size > 5 * 1024 * 1024:
            raise ValidationError("Размер изображения не должен превышать 5MB")
        
        # Проверка формата файла
        img = Image.open(image)
        if img.format not in ['JPEG', 'PNG', 'GIF']:
            raise ValidationError("Поддерживаются только форматы JPEG, PNG и GIF")
        
        # Проверка размеров изображения
        if img.width > 4000 or img.height > 4000:
            raise ValidationError("Максимальный размер изображения 4000x4000 пикселей")
        
        return True
    except Exception as e:
        logger.error(f"Ошибка валидации изображения: {str(e)}")
        raise ValidationError(f"Ошибка при обработке изображения: {str(e)}")

def process_recipe_image(image, recipe_id):
    """
    Обрабатывает изображение рецепта:
    - Изменяет размер для оптимизации
    - Сохраняет в нужную директорию
    - Возвращает путь к сохраненному файлу
    """
    try:
        # Открываем изображение
        img = Image.open(image)
        
        # Изменяем размер для основного изображения (сохраняя пропорции)
        max_size = (1200, 800)
        img.thumbnail(max_size, Image.LANCZOS)
        
        # Создаем буфер для сохранения
        buffer = BytesIO()
        
        # Сохраняем в буфер с оптимизацией
        if img.format == 'JPEG':
            img.save(buffer, format='JPEG', quality=85, optimize=True)
        elif img.format == 'PNG':
            img.save(buffer, format='PNG', optimize=True)
        else:
            img.save(buffer, format=img.format)
        
        # Получаем имя файла и расширение
        file_name = os.path.basename(image.name)
        name, ext = os.path.splitext(file_name)
        
        # Создаем новое имя файла с ID рецепта
        new_name = f"recipe_{recipe_id}_{name}{ext}"
        
        # Путь для сохранения
        path = os.path.join('recipe_images', new_name)
        
        # Сохраняем файл
        buffer.seek(0)
        saved_path = default_storage.save(path, ContentFile(buffer.read()))
        
        # Создаем миниатюру
        img.thumbnail((300, 200), Image.LANCZOS)
        thumb_buffer = BytesIO()
        
        if img.format == 'JPEG':
            img.save(thumb_buffer, format='JPEG', quality=85, optimize=True)
        elif img.format == 'PNG':
            img.save(thumb_buffer, format='PNG', optimize=True)
        else:
            img.save(thumb_buffer, format=img.format)
        
        # Сохраняем миниатюру
        thumb_path = os.path.join('recipe_images', f"thumb_{new_name}")
        thumb_buffer.seek(0)
        default_storage.save(thumb_path, ContentFile(thumb_buffer.read()))
        
        logger.info(f"Изображение для рецепта {recipe_id} успешно обработано и сохранено")
        return saved_path
        
    except Exception as e:
        logger.error(f"Ошибка при обработке изображения для рецепта {recipe_id}: {str(e)}")
        raise ValidationError(f"Ошибка при обработке изображения: {str(e)}")

def process_profile_image(image, user_id):
    """
    Обрабатывает изображение профиля пользователя:
    - Обрезает до квадрата
    - Изменяет размер
    - Сохраняет в нужную директорию
    """
    try:
        # Открываем изображение
        img = Image.open(image)
        
        # Обрезаем до квадрата (берем центральную часть)
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        img = img.crop((left, top, right, bottom))
        
        # Изменяем размер
        img = img.resize((300, 300), Image.LANCZOS)
        
        # Создаем буфер для сохранения
        buffer = BytesIO()
        
        # Сохраняем в буфер с оптимизацией
        if img.format == 'JPEG':
            img.save(buffer, format='JPEG', quality=85, optimize=True)
        elif img.format == 'PNG':
            img.save(buffer, format='PNG', optimize=True)
        else:
            img.save(buffer, format=img.format)
        
        # Получаем имя файла и расширение
        file_name = os.path.basename(image.name)
        name, ext = os.path.splitext(file_name)
        
        # Создаем новое имя файла с ID пользователя
        new_name = f"user_{user_id}_{name}{ext}"
        
        # Путь для сохранения
        path = os.path.join('profile_pictures', new_name)
        
        # Сохраняем файл
        buffer.seek(0)
        saved_path = default_storage.save(path, ContentFile(buffer.read()))
        
        logger.info(f"Изображение профиля для пользователя {user_id} успешно обработано и сохранено")
        return saved_path
        
    except Exception as e:
        logger.error(f"Ошибка при обработке изображения профиля для пользователя {user_id}: {str(e)}")
        raise ValidationError(f"Ошибка при обработке изображения профиля: {str(e)}")
