from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TelField, HiddenField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired(message="Это поле обязательно")])
    phone = TelField('Ваш телефон', validators=[DataRequired(message="Это поле обязательно")])
    address = StringField('Ваш адрес', validators=[DataRequired(message="Это поле обязательно")])
    message = StringField('Дополнительная информация')
    submit = SubmitField('Отправить заказ')
    csrf_token = HiddenField()