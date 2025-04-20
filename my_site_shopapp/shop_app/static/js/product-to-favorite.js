document.addEventListener('DOMContentLoaded', function() {
    const favoriteButton = document.getElementById('favorite-btn');
    const isFavorite = favoriteButton.getAttribute('data-is-favorite') === 'true';

    // Обновляем кнопку при загрузке страницы
    updateFavoriteButton(favoriteButton, isFavorite);

    // Обработчик клика
    favoriteButton.addEventListener('click', function() {
        const productId = this.getAttribute('data-product-pk');
        const isFavorite = this.getAttribute('data-is-favorite') === 'true';

        const method = isFavorite ? 'DELETE' : 'POST';
        const url = isFavorite
            ? `/shop/product/api/favorite/remove/${this.getAttribute('data-favorite-pk')}/`
            : '/shop/product/api/favorite/add/';

        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                product_id: productId,
            }),
        })
        .then(response => {
            if (response.ok) {
                // Проверяем, есть ли тело ответа
                const contentType = response.headers.get('content-type');
                if (contentType && contentType.includes('application/json')) {
                    return response.json();  // Преобразуем ответ в JSON
                } else {
                    return null;  // Пустой ответ
                }
            } else {
                throw new Error('Ошибка при изменении состояния избранного');
            }
            })
        .then(data => {
            // Обновляем состояние кнопки
            const newIsFavorite = !isFavorite;
            favoriteButton.setAttribute('data-is-favorite', newIsFavorite);
            updateFavoriteButton(favoriteButton, newIsFavorite);

            if (newIsFavorite) {
                favoriteButton.setAttribute('data-favorite-pk', data.pk);
            } else {
                favoriteButton.removeAttribute('data-favorite-pk');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Произошла ошибка при выполнении запроса');
        });
    });
});

function updateFavoriteButton(button, isFavorite) {
    const icon = button.querySelector('.favorite-button-icon');
    const tooltip = button.querySelector('.favorite-tooltip');

    if (isFavorite) {
        button.classList.remove('add-to-favorite-btn');
        button.classList.add('remove-to-favorite-btn');
        icon.src = `${STATIC_URL}img/remove-to-favorite-button.png`;
        tooltip.textContent = 'Убрать из избранного';
    } else {
        button.classList.remove('remove-to-favorite-btn');
        button.classList.add('add-to-favorite-btn');
        icon.src = `${STATIC_URL}img/add-to-favorite-button.png`;
        tooltip.textContent = 'Добавить в избранное';
    }
}