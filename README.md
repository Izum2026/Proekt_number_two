🌯 Шаурмечная у Ашота

Современный сайт-визитка для сети шаурмечных, созданный на Flask. Включает меню, админ-панель и адаптивный дизайн.

Технологии:
```bash
-Python
-Flask 
-SQLAlchemy + SQLite
-Bootstrap
-HTML/CSS
```
Клонируй репозиторий:
```bash
git clone https://github.com/Izum2026/Proekt_number_two.git
cd Proekt_number_two
```
Установи зависимости:
```bash
pip install -r requirements.txt
```
Создай файл .env в корне проекта и пропиши настройки:
```bash
SECRET_KEY=твой_ключ
DATABASE=sqlite:///shaurma.db
ADMIN_PASSWORD=пароль_для_админки
```
Запусти сервер:
```bash
python app.py
```
Открой в браузере:
```bash
Сайт: http://127.0.0.1:5000
Админка: http://127.0.0.1:5000/admin
```
```bash
Структура проекта:
Proekt_number_two/
├── app.py                  # Основной файл приложения
├── admin.py                # Настройка админ-панели
├── requirements.txt        # Зависимости
├── .env                    # Секретные настройки (не в Git)
├── .gitignore             
├── templates/             
│   ├── index.html
│   ├── menu.html
│   ├── about_us.html
│   └── admin.html
└── static/                 
    ├── css/
    │   └── style.css
    └── images/             # Фото блюд