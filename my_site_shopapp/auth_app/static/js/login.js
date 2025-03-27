document.addEventListener('DOMContentLoaded', function() {
    // Переключение видимости пароля
    const togglePassword = document.querySelector('#togglePassword');
    const passwordField = document.querySelector('#id_password');

    if (togglePassword && passwordField) {
        togglePassword.addEventListener('click', function() {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    }

    // Добавление классов к полям формы
    const formFields = ['username', 'password'];

    formFields.forEach(field => {
        const input = document.querySelector(`#id_${field}`);
        if (input) {
            input.classList.add('form-input');
            input.placeholder = input.placeholder || `Введите ${field.replace('_', ' ')}`;
        }
    });

    // Подсветка ошибок
    const errorElements = document.querySelectorAll('.error-message');
    errorElements.forEach(error => {
        const inputId = error.id.replace('error_', '');
        const inputField = document.querySelector(`#${inputId}`);
        if (inputField) {
            inputField.classList.add('error-field');
        }
    });
});