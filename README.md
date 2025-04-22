# Интернет-магазин Django-ShopApp

![Логотип](static/images/logo.png)  
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.1.4-brightgreen.svg)](https://djangoproject.com)

Полнофункциональный интернет-магазин с системой заказов, корзиной, избранным и панелью администратора.

## 🌟 Особенности

- 🛒 Система корзины товаров
- ❤️ Система избранных товаров
- 🚚 Оформление заказа
- 🔐 Аутентификация через пароль
- 📦 Панель управления товарами для продавцов
- 📱 Адаптивный дизайн для всех устройств
- ⚡️ Производительность (кеширование, оптимизация запросов)

## 🛠 Технологический стек

**Backend:**
- Python 3.10+
- Django 5.1.4
- Django REST Framework
- SQLite

**Инфраструктура:**
- Docker

## 🚀 Установка

### Локальная разработка

1. Клонируйте репозиторий:
   ```bash
   git clone https://gitlab.com/projects-afox-portfolio/django-shopapp-studentproject.git
   cd .\my_site_shopapp\
   
2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    venv\Scripts\activate
   
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   
4. Примените миграции:
   ```bash
   python manage.py migrate
   
5. Запустите сервер:
   ```bash
   python manage.py runserver
   
## 📂 Структура проекта
   ```bash
   Django-ShopApp-StudentProject/
   ├── my_site_shopapp/
   │   ├── auth_app           # Аутентификация
   │   ├── media/
   │   │   ├──products        # Папка медиафайлов продуктов
   │   │   └──profiles        # Папка медиафайлов пользователей
   │   ├── my_site_shopapp
   │   ├── profiles_app       # Профили пользователей
   │   │   ├── shop_app/      # Магазин
   │   │   ├── static         # Статические файлы
   │   │   ├── templates      # Шаблоны
   │   │   ├── __init__.py
   │   ├── shop_app_api       # API магазина
   │   ├── .stilelintrc.json  # Конфиг линтера
   │   ├── db.sqlite3
   │   ├── manage.py
   │   └── pyproject.toml     # Конфиг плагинов
   ├── Dockerfile
   └── README.md
   ```
## 🌐 API Endpoints
| Endpoint                                     | Метод  | Описание                   |
|----------------------------------------------|--------|----------------------------|
| `shop/product/api/cart/add/`                 | POST   | Добавить товар в корзину   |
| `shop/product/api/cart/remove/<int:pk>`      | DELETE | Удалить товар из корзины   |
| `shop/ product/api/favorite/add/`            | POST   | Добавить в избранное       |
| `shop/product/api/favorite/remove/<int:pk>/` | DELETE | Удалить из избранного      |
| `shop/orders/api/create/`                    | POST   | Создать заказ              |
| `shop/checkout/api/selected-products/`       | POST   | Работа с товарами в сессии |

## ✉️ Контакты
[@AFoxq](https://t.me/AFoxq) - bourraska@gmail.com

[Ссылка на проект](https://gitlab.com/projects-afox-portfolio/django-shopapp-studentproject)