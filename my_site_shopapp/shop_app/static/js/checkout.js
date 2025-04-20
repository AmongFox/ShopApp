document.addEventListener('DOMContentLoaded', function() {
    const selectedProducts = JSON.parse(sessionStorage.getItem('selectedProducts') || '[]');

    if (selectedProducts.length > 0) {
        fetch('http://127.0.0.1:8000/shop/checkout/api/selected-products/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                selected_products: selectedProducts
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Получены товары:', data.products);
            // Обновляем данные на странице
            updateOrderSummary(data.products, data.total_price);
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Ошибка при загрузке данных заказа');
        });
    }
});

function updateOrderSummary(products, totalPrice) {
    const orderItems = document.getElementById('order-items');
    const orderTotal = document.querySelector('.order-total h3');

    // Очищаем предыдущие товары
    orderItems.innerHTML = '';

    // Добавляем новые товары
    products.forEach(product => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'order-item';
        itemDiv.innerHTML = `
            <h3>${product.name}</h3>
            <p>${product.price} ₽</p>
        `;
        orderItems.appendChild(itemDiv);
    });

    // Обновляем итоговую сумму
    orderTotal.textContent = `Итого: ${totalPrice} ₽`;
}