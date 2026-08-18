from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TelField, HiddenField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    email = EmailField('Ваш логин', validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                                Email(message="Некорректный email")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Это поле обязательно для заполнения")])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired(message="Это поле обязательно")])
    phone = TelField('Ваш телефон', validators=[DataRequired(message="Это поле обязательно")])
    address = StringField('Ваш адрес', validators=[DataRequired(message="Это поле обязательно")])
    message = StringField('Дополнительная информация')
    submit = SubmitField('Отправить заказ')
    csrf_token = HiddenField()


class RegisterForm(FlaskForm):
    email = EmailField("Ваш логин", validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                                Email(message="Некорректный email")])
    password = PasswordField("Пароль", validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                                   Length(min=6, message="Пароль должен содержать минимум 6 символов")])
    password_again = PasswordField("Повторите пароль",
                                   validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                               EqualTo("password", message="Пароли не совпадают")])
    name = StringField("Ваше имя",
                       validators=[DataRequired(), Length(min=2, max=50, message="Слишком короткое или длинное имя")])
    submit = SubmitField("Зарегистрироваться")
