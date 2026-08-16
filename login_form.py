from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField('Ваш логин', validators=[DataRequired(message="Это поле обязательно для заполнения"), Email(message="Некорректный email")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Это поле обязательно для заполнения")])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
