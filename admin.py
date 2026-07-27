import os
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import FileUploadField
from werkzeug.utils import secure_filename
from flask import redirect, url_for, session


class ProtectedModelView(ModelView):
    def is_accessible(self):
        return session.get('admin_logged_in')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login'))


class ProtectedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return session.get('admin_logged_in')

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

    column_list = ('name', 'price', 'category', 'image_preview')
    column_formatters = {
        'image_preview': lambda a, b, c, d: f'<img src="/static/images/{c.image}" width="50">'
    }


def init_admin(app, db):
    admin = Admin(
        app,
        name='Админка шаурмечной',
        index_view=ProtectedAdminIndexView()
    )

    from app import MenuItem

    admin.add_view(MenuItemAdmin(MenuItem, db.session))
    return admin
