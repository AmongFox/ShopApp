document.addEventListener('DOMContentLoaded', function() {
    const cartButtons = document.querySelectorAll('.add-to-cart-btn');

    cartButtons.forEach(cartButton => {
        const isCart = cartButton.getAttribute('data-is-cart') === 'true';

        // Обновляем кнопку при загрузке страницы
        updateCartButton(cartButton, isCart);

        // Обработчик клика
        cartButton.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-pk');
            const isCart = this.getAttribute('data-is-cart') === 'true';

            const method = isCart ? 'DELETE' : 'POST';
            const url = isCart
                ? `/shop/product/api/cart/remove/${this.getAttribute('data-cart-pk')}/`
                : '/shop/product/api/cart/add/';

            fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: 1,
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
                    throw new Error('Ошибка при изменении состояния корзины');
                }
            })
            .then(data => {
                // Обновляем состояние кнопки
                const newIsCart = !isCart;
                cartButton.setAttribute('data-is-cart', newIsCart);
                updateCartButton(cartButton, newIsCart);

                if (newIsCart) {
                    cartButton.setAttribute('data-cart-pk', data.pk);
                } else {
                    cartButton.removeAttribute('data-cart-pk');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при выполнении запроса');
            });
        });
    });
});

function updateCartButton(button, isCart) {
    if (isCart) {
        button.classList.remove('add-to-cart-btn');
        button.classList.add('remove-to-cart-btn');
        button.textContent = 'Удалить из корзины';
    } else {
        button.classList.remove('remove-to-cart-btn');
        button.classList.add('add-to-cart-btn');
        button.textContent = 'Добавить в корзину';
    }
}