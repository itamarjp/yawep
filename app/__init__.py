from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_login import current_user, login_user


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

#from app.controllers.default import send_async_linux_task

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


app.config.from_object('config')

db = SQLAlchemy(app,session_options={"expire_on_commit": False})
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
#login.login_view = 'login' #login enabled  for all pages

from app.controllers import default
from app.controllers.default import send_async_linux_task

from app.models import tables

from app.models.tables import User
from app.models.tables import Domains
from app.models.tables import Emails
from app.models.tables import Databases
from app.models.tables import Ftpaccounts


#flask-admin
admin = Admin(app, name='yawep', template_mode='bootstrap3')

class UserView(ModelView):
    can_create = True
    can_delete = False
    page_size = 50
    can_set_page_size = True
    column_list = ['name','email', 'username',  'password']
    column_exclude_list = ['password', ]
    column_editable_list = ['name', 'email','password']
    form_excluded_columns = ['domains',]
    create_modal = True
    edit_modal = True
    column_searchable_list = ['username','email']
    column_filters = ['username','email']
    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)

class DomainsView(ModelView):
    create_modal = True
    edit_modal = True
    can_create = True
    can_delete = False
    page_size = 50
    can_set_page_size = True
    column_list = ['name']
    column_exclude_list = ['Databases','Emails','Ftpaccounts' ,'User',]
    column_editable_list = [] #popup edit
    form_excluded_columns = ['databases','emails','ftpaccounts' ,]

#    column_searchable_list = ['name']
#    column_select_related_list = (User.id)
    column_filters = ['name']
#    form_ajax_refs = {
#    'user': {
#        'fields': ['username'],
#        'page_size': 100
#    }
#    }

    #form_widget_args = {
    #    'user':{'readonly':True},
    #}
    #from flask_admin.form.rules import Field
    #form_edit_rules = [
    #    CustomizableField('user', field_args={'readonly': True}),
    #    ]

    def on_form_prefill(self, form, id):
        form.user.render_kw = {'readonly': True}
        form.name.render_kw = {'readonly': True}

    def after_model_change(self, form, model, is_created):
       if is_created:
          send_async_linux_task(msg = model.serialize, queue="domains", action = "new")
       else:
          send_async_linux_task(msg = model.serialize, queue="domains", action = "edit")
    def after_model_delete(self, model):
      send_async_linux_task(msg = model.serialize, queue="domains", action = "delete")

    def __init__(self, session, **kwargs):
        super(DomainsView, self).__init__(Domains, session, **kwargs)

class DatabasesView(ModelView):
    create_modal = True
    edit_modal = True
    can_create = True
    can_delete = True
    page_size = 50
    can_set_page_size = True
    column_list = ['username','domain.name']
    column_exclude_list = ['password','domain']
    column_editable_list = ['password']
    form_excluded_columns = []
    column_searchable_list = ['databasename']
    column_filters = ['databasename']
    #form_widget_args = {
    #    'databasename':{'disabled':True},
    #    'username':{'disabled':True},
    #    'domain':{'disabled':True},
    #}
    def on_form_prefill(self, form, id):
        form.databasename.render_kw = {'readonly': True}
        form.username.render_kw = {'readonly': True}
        form.domain.render_kw = {'readonly': True}
    form_ajax_refs = {
      'domain': {
        'fields': ['name'],
        'page_size': 100
       }
      }

    def after_model_change(self, form, model, is_created):
       if is_created:
          send_async_linux_task(msg = model.serialize, queue="databases", action = "new")
       else:
          send_async_linux_task(msg = model.serialize, queue="databases", action = "edit")
    def after_model_delete(self, model):
      send_async_linux_task(msg = model.serialize, queue="databases", action = "delete")

    def __init__(self, session, **kwargs):
        super(DatabasesView, self).__init__(Databases, session, **kwargs)

class FtpaccountsView(ModelView):
    create_modal = True
    edit_modal = True
    can_create = True
    can_delete = True
    page_size = 50
    can_set_page_size = True
    column_list = ['username','domain.name']
    column_exclude_list = ['password','domain']
    column_editable_list = ['password']
    form_excluded_columns = []
    column_searchable_list = ['username','domain.name']
    column_filters = ['username','domain.name']
    #form_widget_args = {
    #    'databasename':{'disabled':True},
    #    'username':{'disabled':True},
    #    'domain':{'disabled':True},
    #}
    def on_form_prefill(self, form, id):
        form.username.render_kw = {'readonly': True}
        form.domain.render_kw = {'readonly': True}
    form_ajax_refs = {
      'domain': {
        'fields': ['name'],
        'page_size': 100
       }
      }


    def after_model_change(self, form, model, is_created):
       if is_created:
          send_async_linux_task(msg = model.serialize, queue="ftpaccounts", action = "new")
       else:
          send_async_linux_task(msg = model.serialize, queue="ftpaccounts", action = "edit")
    def after_model_delete(self, model):
      send_async_linux_task(msg = model.serialize, queue="ftpaccounts", action = "delete")

    def __init__(self, session, **kwargs):
        super(FtpaccountsView, self).__init__(Ftpaccounts, session, **kwargs)


class EmailsView(ModelView):
    create_modal = True
    edit_modal = True
    can_create = True
    can_delete = True
    page_size = 50
    can_set_page_size = True
    column_list = ['full_email', 'username','domain.name']
    column_exclude_list = ['password','domain']
    column_editable_list = ['password']
    form_excluded_columns = []
    column_searchable_list = ['username']
    column_filters = ['username']
    #form_widget_args = {
    #    'databasename':{'disabled':True},
    #    'username':{'disabled':True},
    #    'domain':{'disabled':True},
    #}
#   column_choices = { 'domain': [('domain.id', 'domain.name'),]}

    def on_form_prefill(self, form, id):
        form.username.render_kw = {'readonly': True}
        form.domain.render_kw = {'readonly': True}
    form_ajax_refs = {'domain': { 'fields': ['name'], 'page_size': 100   }      }


    def after_model_change(self, form, model, is_created):
       if is_created:
          send_async_linux_task(msg = model.serialize, queue="emails", action = "new")
       else:
          send_async_linux_task(msg = model.serialize, queue="emails", action = "edit")
    def after_model_delete(self, model):
      send_async_linux_task(msg = model.serialize, queue="emails", action = "delete")

    def __init__(self, session, **kwargs):
        super(EmailsView, self).__init__(Emails, session, **kwargs)

    #def is_accessible(self):
    #    return login.current_user.is_authenticated

    #def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
    #    return redirect(url_for('login', next=request.url))


from flask_admin import Admin, BaseView, expose


class MyView(BaseView):
 @expose('/')
 def index(self):
    return redirect('/admin/logout')

#admin.add_view(ModelView(User, db.session))
admin.add_view(UserView(db.session))
admin.add_view(DomainsView(db.session))

admin.add_view(DatabasesView(db.session))
admin.add_view(EmailsView(db.session))
admin.add_view(FtpaccountsView(db.session))
admin.add_view(MyView(name='Logout', endpoint='logout', category='Logout'))


db.create_all(app=app)

