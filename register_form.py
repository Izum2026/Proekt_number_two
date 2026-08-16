from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegisterForm(FlaskForm):
    email = EmailField("Ваш логин", validators=[DataRequired(message="Это поле обязательно для заполнения"), Email(message="Некорректный email")])
    password = PasswordField("Пароль", validators=[DataRequired(message="Это поле обязательно для заполнения"),
                                                   Length(min=6, message="Пароль должен содержать минимум 6 символов")])
    password_again = PasswordField("Повторите пароль",
                                   validators=[DataRequired(message="Это поле обязательно для заполнения"), EqualTo("password", message="Пароли не совпадают")])
    name = StringField("Ваше имя",
                       validators=[DataRequired(), Length(min=2, max=50, message="Слишком короткое или длинное имя")])
    submit = SubmitField("Зарегистрироваться")
