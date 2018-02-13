from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)




@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)

from app.controllers import default
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
    page_size = 50
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
    can_create = True
    can_delete = False
    page_size = 50
    column_list = ['name']
    column_exclude_list = ['Databases','Emails','Ftpaccounts' ,'User',]
    column_editable_list = ['name',]
    form_excluded_columns = ['databases','emails','ftpaccounts' ,]
    column_searchable_list = ['name']
#    column_select_related_list = (User.id)
    column_filters = ['name']
    form_ajax_refs = {
    'user': {
        'fields': ['name'],
        'page_size': 100
    }
    }

    create_modal = True
    edit_modal = True
    def __init__(self, session, **kwargs):
        super(DomainsView, self).__init__(Domains, session, **kwargs)

class DatabasesView(ModelView):
    can_create = True
    can_delete = True
    page_size = 50
    column_list = []
    column_exclude_list = ['username','password','domain']
    column_editable_list = ['password']
    form_excluded_columns = []
    column_searchable_list = ['databasename']
    column_filters = ['databasename']
    def after_model_change(self, form, model, is_created):
      pass
    def after_model_delete(self, model):
      pass
    def on_model_delete(self, model):
      print ("removing")
      print (type(model))
      print (model.serialize)

    xform_ajax_refs = {
    'domains': {
        'fields': ['domains'],
        'page_size': 100
     }
    }

    create_modal = True
    edit_modal = True
    def __init__(self, session, **kwargs):
        super(DatabasesView, self).__init__(Databases, session, **kwargs)





#admin.add_view(ModelView(User, db.session))
admin.add_view(UserView(db.session))
admin.add_view(DomainsView(db.session))
admin.add_view(DatabasesView(db.session))
#admin.add_view(ModelView(Databases, db.session))
admin.add_view(ModelView(Emails, db.session))
admin.add_view(ModelView(Ftpaccounts, db.session))


#from app.controllers import adminpages
db.create_all(app=app)

