import os
import json
import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from order_form import OrderForm

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


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    client_name = db.Column(db.String(100))
    phone = db.Column(db.String(25))
    address = db.Column(db.String(400))
    message = db.Column(db.String(400))
    items_json = db.Column(db.Text)
    status = db.Column(db.String(20), default='Новый')
    total_summa = db.Column(db.Float)


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
        data = request.get_json()
        if not data:
            abort(400, description="No data")
        quantity = data['quantity']

        cart = session.get('cart', {})
        if str(item_id) not in cart:
            abort(404, description="No item")

        if quantity == 0:
            del cart[str(item_id)]
        else:
            cart[str(item_id)] = quantity
        session['cart'] = cart
        return {"message": "Количество обновлено"}, 200


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


@app.route('/order', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    cart = session.get('cart', {})
    items = CartResource.get(cart)
    if not cart:
        return redirect('/cart')
    if form.validate_on_submit():
        cart = session.get('cart', {})

        items_list = []
        total_summa = 0
        for key, _ in cart.items():
            item = db.session.get(MenuItem, key)
            if item is None:
                continue
            total_summa += int(item.price) * cart[key]
            items_list.append({
                "id": item.id,
                "name": item.name,
                "price": str(item.price),
                "quantity": cart[key],
                "category": item.category
            })
        order = Order(
            time=datetime.datetime.now(),
            client_name=form.name.data,
            phone=form.phone.data,
            address=form.address.data,
            message=form.message.data,
            items_json=json.dumps(items_list, ensure_ascii=False),
            status='Новый',
            total_summa=total_summa
        )
        db.session.add(order)
        db.session.commit()
        session['cart'] = {}
        return redirect('/order_success')

    return render_template('order.html', form=form, result=items)


@app.route('/order_success')
def order_success():
    return render_template('order_success.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
