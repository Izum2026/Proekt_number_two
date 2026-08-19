import os
import json
import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, session, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api, Resource
from forms import OrderForm
from models import MenuItem, User, Order
from extensions import db
from forms import RegisterForm
from forms import LoginForm
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')
db.init_app(app)
swagger = Swagger(app)

from admin import init_admin

init_admin(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.errorhandler(404)
def not_found_error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error_500(error):
    return render_template('500.html'), 500


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
def menu_page():
    return render_template('menu.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            user = User(
                name=form.name.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Регистрация успешна!', 'success')
            return redirect('/login')
        else:
            flash('Этот email уже используется.', 'danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        else:
            flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form)


@app.route('/profile')
@login_required
def profile():
    orders = [
        {
            'order': order,
            'items': json.loads(order.items_json)
        }
        for order in current_user.orders
    ]
    return render_template('profile.html', user=current_user, orders=orders)


class MenuListResource(Resource):
    def get(self):
        """
        GET /api/menu
        Список всех категорий с товарами
        ---
        tags:
          - menu
        responses:
          200:
            description: Успешный ответ
            examples:
              application/json:
                [
                  {
                    "category": "Шаурма",
                    "items": [
                      {
                        "id": 1,
                        "name": "Классическая",
                        "price": "280",
                        "category": "Шаурма",
                        "image": "classic_shaurma.jpg"
                      },
                      {
                        "id": 2,
                        "name": "Барбекю",
                        "price": "300",
                        "category": "Шаурма",
                        "image": "barbecue_shaurma.jpg"
                      },
                      {
                        "id": 5,
                        "name": "Острая",
                        "price": "290",
                        "category": "Шаурма",
                        "image": "spicy_shaurma.jpg"
                      }
                    ]
                  },
                  {
                    "category": "Картошка",
                    "items": [
                      {
                        "id": 3,
                        "name": "Фри",
                        "price": "150",
                        "category": "Картошка",
                        "image": "potato_1.jpg"
                      },
                      {
                        "id": 4,
                        "name": "По-деревенски",
                        "price": "160",
                        "category": "Картошка",
                        "image": "potato_2.png"
                      }
                    ]
                  }
                ]
          500:
            description: Ошибка сервера
        """
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
        """
        GET /api/cart
        Список товаров с корзины
        ---
        tags:
          - cart get
        responses:
          200:
            description: Успешный ответ
            examples:
              application/json:
                 {
                  "items": [
                    {
                      "id": 2,
                      "name": "Барбекю",
                      "price": "300",
                      "image": "barbecue_shaurma.jpg",
                      "quantity": 1
                    },
                    {
                      "id": 5,
                      "name": "Острая",
                      "price": "290",
                      "image": "spicy_shaurma.jpg",
                      "quantity": 1
                    }
                  ],
                  "score": 2,
                  "summa": 590
                }
          500:
            description: Ошибка сервера
        """
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
        """
        POST /api/cart
        Список товаров с корзины
        ---
        tags:
          - cart post
        responses:
          200:
            description: Успешный ответ
            examples:
              application/json:
                 {"1": 2, "7": 1}
          400:
            description: Неверный запрос
          404:
            description: Товар не найден
        """
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


api.add_resource(CartResource, '/api/cart')


class CartItemResource(Resource):
    def delete(self, item_id):
        """
        DELETE /api/cart/{item_id}
        Удаление товара из корзины
        ---
        tags:
          - cart
        responses:
          200:
            description: Успешный ответ
            examples:
              application/json:
                 {"message": "Товар удалён"}
          404:
            description: Товар не найден
        """
        cart = session.get('cart', {})
        if str(item_id) not in cart:
            abort(404, description="No item")
        del cart[str(item_id)]
        session['cart'] = cart
        return {"message": "Товар удалён"}, 200

    def put(self, item_id):
        """
        PUT /api/cart/{item_id}
        Изменение количества товара в корзине
        ---
        tags:
          - cart
        responses:
          200:
            description: Успешный ответ
            examples:
              application/json:
                 {"message": "Количество обновлено"}
          400:
            description: Неверный запрос
          404:
            description: Товар не найден
        """
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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.is_admin and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/admin')
        flash('Доступ запрещён')
    return render_template('login.html', form=form)


@app.route('/cart')
def basket():
    return render_template('cart.html')


@app.route('/order', methods=['GET', 'POST'])
@login_required
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
            total_summa += item.price * cart[key]
            items_list.append({
                "id": item.id,
                "name": item.name,
                "price": item.price,
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
            total_summa=total_summa,
            user_id=current_user.id
        )
        db.session.add(order)
        db.session.commit()
        session['cart'] = {}
        return redirect('/order_success')

    return render_template('order.html', form=form, result=items)


@app.route('/order_success')
@login_required
def order_success():
    return render_template('order_success.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
