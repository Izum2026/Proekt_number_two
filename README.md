🌯 Шаурмечная у Ашота

Современный сайт-визитка для сети шаурмечных, созданный на Flask. Включает меню, админ-панель и адаптивный дизайн:
```
Регистрация и авторизация пользователей
Корзина с возможностью добавления, удаления, изменения количества товаров
Оформление заказа с сохранением в базу данных
Личный кабинет с историей заказов
Админ-панель для управления меню и заказами
REST API с документацией Swagger
```
Технологии:
```bash
-Python
-Flask 
-SQLAlchemy + SQLite
-Bootstrap
-HTML/CSS/JS
```
Клонируй репозиторий:
```
git clone https://github.com/Izum2026/Proekt_number_two.git
cd Proekt_number_two
```
Установи зависимости:
```
pip install -r requirements.txt
```
Создай файл .env в корне проекта и пропиши настройки:
```
SECRET_KEY=твой_ключ
DATABASE=sqlite:///shaurma.db
```
Запусти сервер:
```bash
python app.py
```
Открой в браузере:
```
Сайт: http://127.0.0.1:5000
Админка: http://127.0.0.1:5000/admin
```
Создание администратора

```bash
python
>>> from app import app, db
>>> from models import User
>>> with app.app_context():
...     admin = User(name="Admin", email="example@shaurma.ru", is_admin=True)
...     admin.set_password("твой пароль")
...     db.session.add(admin)
...     db.session.commit()
```
```
Структура проекта:
Proekt_number_two/
├── app.py                  # Основной файл приложения
├── admin.py                # Настройка админ-панели
├── models.py               # Модели
├── forms.py                # Формы
├── extensions.py    
├── requirements.txt        # Зависимости
├── .env                    # Секретные настройки (не в Git)
├── .gitignore             
├── templates/             
│   ├── index.html
│   ├── menu.html
│   ├── about_us.html
│   ├── admin.html
│   ├── 404.html
│   ├── 500.html
│   ├── login.html
│   ├── order.html
│   ├── order_success.html
│   ├── profile.html
│   ├── register.html
│   └── cart.html
├── static/                 
│   ├── css/
│   │ └── style.css
│   └── images/             # Фото блюд
└── instance/
    └── shaurma.db