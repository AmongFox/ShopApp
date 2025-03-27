document.addEventListener('DOMContentLoaded', function() {
    // Переключение видимости пароля
    const togglePassword1 = document.querySelector('#togglePassword1');
    const togglePassword2 = document.querySelector('#togglePassword2');
    const passwordField1 = document.querySelector('#id_password');
    const passwordField2 = document.querySelector('#id_password_confirm');

    if (togglePassword1 && passwordField1) {
        togglePassword1.addEventListener('click', function() {
            const type = passwordField1.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField1.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    }

    if (togglePassword2 && passwordField2) {
        togglePassword2.addEventListener('click', function() {
            const type = passwordField2.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField2.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    }

    // Добавление классов к полям формы
    const formFields = ['username', 'email', 'phone_number', 'password', 'password_confirm'];

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