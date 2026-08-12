import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
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


class MenuListResource(Resource):
    def get(self):
        items_menu = MenuItem.query.all()
        categories = {}
        result = []
        for item in items_menu:
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
        return result


api.add_resource(MenuListResource, '/api/menu')


class CartResource(Resource):

    def get(self):
        cart = session.get('cart', {})
        items = []
        score = 0
        summa = 0
        if not cart:
            return {'items': [], 'score': 0, 'summa': 0}
        for item_id, quantity in cart.items():
            item = db.session.get(MenuItem, item_id)
            if item is None:
                continue
            items.append({
                "id": item.id,
                "name": item.name,
                "price": str(item.price),
                "image": item.image,
                "quantity": quantity
            })
            score += quantity
            summa += quantity * item.price
        return {'items': items, 'score': score, 'summa': summa}

    def post(self):
        data = request.get_json()
        if not data:
            abort(400, description="No data")

        item_id = data['item_id']
        quantity = data.get('quantity', 1)
        cart = session.get('cart', {})

        if item_id in cart:
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity

        session['cart'] = cart
        return cart

    def delete(self):
        session['cart'] = {}
        return {"message": "Корзина очищена"}


api.add_resource(CartResource, '/api/cart')


class CartItemResource(Resource):
    def delete(self, item_id):
        cart = session.get('cart', {})
        if str(item_id) not in cart:
            abort(404, description="No item")
        del cart[str(item_id)]
        session['cart'] = cart
        return {"message": "Товар удалён"}, 200

    def put(self, item_id):
        ...


api.add_resource(CartItemResource, '/api/cart/<int:item_id>')


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


@app.route('/cart')
def basket():
    return render_template('cart.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
