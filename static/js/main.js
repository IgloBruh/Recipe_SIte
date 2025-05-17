// Основной JavaScript файл для платформы обмена рецептами

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всплывающих подсказок Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Обработка избранного
    setupFavoriteButtons();
    
    // Предпросмотр изображений при загрузке
    setupImagePreview();
    
    // Валидация форм
    setupFormValidation();
    
    // Настройка фильтров
    setupFilters();
});

// Функция для обработки кнопок избранного
function setupFavoriteButtons() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    
    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const recipeId = this.dataset.recipeId;
            const isFavorite = this.classList.contains('active');
            
            // Отправка запроса к API
            fetch(`/api/favorites/`, {
                method: isFavorite ? 'DELETE' : 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    recipe: recipeId
                })
            })
            .then(response => {
                if (response.ok) {
                    // Переключение состояния кнопки
                    this.classList.toggle('active');
                    const icon = this.querySelector('i');
                    if (icon) {
                        icon.classList.toggle('fas');
                        icon.classList.toggle('far');
                    }
                    
                    // Показать уведомление
                    showToast(isFavorite ? 'Рецепт удален из избранного' : 'Рецепт добавлен в избранное');
                } else {
                    throw new Error('Ошибка при обновлении избранного');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                showToast('Произошла ошибка. Пожалуйста, попробуйте снова.', 'error');
            });
        });
    });
}

// Функция для предпросмотра изображений
function setupImagePreview() {
    const imageInput = document.getElementById('id_image');
    const imagePreview = document.getElementById('image-preview');
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
}

// Функция для валидации форм
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// Функция для настройки фильтров
function setupFilters() {
    const filterForm = document.getElementById('filter-form');
    
    if (filterForm) {
        // Обработка изменений в форме фильтров
        const filterInputs = filterForm.querySelectorAll('input, select');
        
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                filterForm.submit();
            });
        });
        
        // Кнопка сброса фильтров
        const resetButton = document.getElementById('reset-filters');
        
        if (resetButton) {
            resetButton.addEventListener('click', function(e) {
                e.preventDefault();
                
                filterInputs.forEach(input => {
                    if (input.type === 'checkbox' || input.type === 'radio') {
                        input.checked = false;
                    } else {
                        input.value = '';
                    }
                });
                
                filterForm.submit();
            });
        }
    }
}

// Функция для отображения уведомлений
function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container');
    
    if (!toastContainer) {
        const container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast ${type === 'error' ? 'bg-danger' : 'bg-success'} text-white`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto">${type === 'error' ? 'Ошибка' : 'Успешно'}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    document.querySelector('.toast-container').appendChild(toast);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Автоматическое удаление после закрытия
    toast.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// Функция для получения значения cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция для отправки рейтинга
function submitRating(recipeId, rating) {
    fetch(`/api/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            recipe: recipeId,
            rating: rating,
            comment: document.getElementById('review-comment').value
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Ошибка при отправке отзыва');
    })
    .then(data => {
        showToast('Ваш отзыв успешно добавлен');
        // Перезагрузка страницы для отображения нового отзыва
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    })
    .catch(error => {
        console.error('Ошибка:', error);
        showToast('Произошла ошибка при отправке отзыва. Пожалуйста, попробуйте снова.', 'error');
    });
}
