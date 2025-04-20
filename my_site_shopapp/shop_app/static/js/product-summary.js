document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.product-checkbox');
    const itemsCountElement = document.querySelector('.items-count');
    const totalPriceElement = document.querySelector('.total-price');
    const checkoutButton = document.getElementById('checkout-btn');

    function updateSummary() {
        let totalItems = 0;
        let totalPrice = 0;
        const selectedProducts = [];

        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                totalItems++;
                totalPrice += parseFloat(checkbox.dataset.productPrice);
                selectedProducts.push(checkbox.dataset.productId);
            }
        });

        itemsCountElement.textContent = `Товары (${totalItems})`;
        totalPriceElement.textContent = `${totalPrice.toFixed(2)} ₽`;
        checkoutButton.disabled = totalItems === 0;

        // Сохраняем выбранные товары в sessionStorage
        sessionStorage.setItem('selectedProducts', JSON.stringify(selectedProducts));
    }

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSummary);
    });

    // Обработчик для кнопки оформления заказа
    checkoutButton.addEventListener('click', function() {
        const selectedProducts = JSON.parse(sessionStorage.getItem('selectedProducts') || '[]');
        if (selectedProducts.length > 0) {
            window.location.href = '/shop/checkout/';
        }
    });

    updateSummary();
});