import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, request, session, flash

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')
db = SQLAlchemy(app)


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'{self.name} ({self.price}₽)'


from admin import init_admin

init_admin(app, db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
def menu_page():
    return render_template('menu.html')


@app.route('/api/menu', methods=['GET'])
def menu():
    items = MenuItem.query.all()
    categories = {}
    result = []
    for item in items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)

    for category, items_list in categories.items():
        items = []
        for item in items_list:
            items.append({
                "id": item.id,
                "name": item.name,
                "price": str(item.price),
                "category": item.category,
                "image": item.image})
        result.append({
            "category": category,
            "items": items})
    return jsonify(result), 200


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('password') == os.getenv('ADMIN_PASSWORD'):
            session['admin_logged_in'] = True
            return redirect('/admin')
        flash('Неверный пароль')
    return render_template('admin.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
