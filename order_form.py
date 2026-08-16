from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TelField, HiddenField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    phone = TelField('Ваш телефон', validators=[DataRequired()])
    address = StringField('Ваш адрес', validators=[DataRequired()])
    message = StringField('Дополнительная информация', validators=[DataRequired()])
    submit = SubmitField('Отправить заказ')
    csrf_token = HiddenField()