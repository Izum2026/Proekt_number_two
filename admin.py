import os
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField
from werkzeug.utils import secure_filename
from flask import redirect, url_for
from flask_login import current_user


class ProtectedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))


class ProtectedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))


class MenuItemAdmin(ProtectedModelView):
    form_extra_fields = {
        'image_upload': FileUploadField(
            label='Картинка блюда',
            base_path=os.path.join('static', 'images'),
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif'],
            namegen=lambda obj, file_data: secure_filename(file_data.filename)
        )
    }

    def on_model_change(self, form, model, is_created):
        if form.image_upload.data:
            model.image = form.image_upload.data.filename

    column_list = ('name', 'price', 'category', 'image')
    column_formatters = {
        'image_preview': lambda a, b, c, d: f'<img src="/static/images/{c.image}" width="50">'
    }


class OrdersAdmin(ProtectedModelView):
    column_list = ('client_name', 'phone', 'address', 'message', 'items_json', 'status', 'total_summa')
    form_choices = {
        'status': [
            ('Новый', 'Новый'),
            ('Готовится', 'Готовится'),
            ('Готов к выдаче', 'Готов к выдаче'),
            ('Доставлен', 'Доставлен'),
            ('Отменён', 'Отменён'),
        ]
    }


def init_admin(app, db):
    admin = Admin(
        app,
        name='Админка шаурмечной',
        index_view=ProtectedAdminIndexView()
    )

    from models import MenuItem, Order

    admin.add_view(MenuItemAdmin(MenuItem, db.session))
    admin.add_view(OrdersAdmin(Order, db.session))
    return admin
