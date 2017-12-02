from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from app import app
from app import db
from app import login_manager
from flask_login import login_user
from flask_login import logout_user

from app.models.tables import User
from app.models.forms import LoginForm
from app.models.forms import NewUserForm

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from flask import request
from flask import jsonify
from flask import abort

from json import dumps
from flask import make_response

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/index")
@app.route("/home")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    form_login = LoginForm()
    if form_login.validate_on_submit():
        user = User.query.filter_by(username=form_login.username.data).first()
        if user and user.password == form_login.password.data:
            login_user(user)
            return redirect(url_for("index"))
            flash("Logged in.")
        else:
            flash("Ivalid login.")
    return render_template('login.html', form=form_login)

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("login"))

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    return True


#http://localhost/api/users
@app.route('/api/users', methods = ['GET']) #(retrieve list)
@auth.login_required
def get_ALL_users():
   users = User.query.all()
   if not users:
      abort(404)
   response = jsonify([i.serialize for i in users])
   response.status_code = 200
   return response

#http://localhost/api/users/123
@app.route('/api/users/<int:user_id>', methods = ['GET']) #(retrieve user 123)
@auth.login_required
def get_user(user_id):
       app.logger.debug('metodo get')
       user = User.query.filter_by(id = user_id).first_or_404()
       response = jsonify(user.serialize)
       response.status_code = 200
       return response

@app.route('/api/users', methods = ['POST'])  #(create a new user, from data provided with the request)
@auth.login_required
def new_user():
    name =  str(request.json.get('name', ''))
    email =  str(request.json.get('email', ''))
    username =  str(request.json.get('username', ''))
    password =  str(request.json.get('password', ''))
    if username is None or password is None or email is None:
        app.logger.debug('missing arguments')
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        app.logger.debug('usuario ja existe')
        abort(400) # existing user
    if User.query.filter_by(email = email).first() is not None:
        app.logger.debug('email ja existe')
        abort(400) # existing user registered with email
    user = User(name = name,  email = email, username = username)
    user.hash_password(password)
    user.save()
    return jsonify(user.serialize), 201, {'Location': url_for('get_user', user_id = user.id, _external = True)}

#http://localhost/api/users/123
@app.route('/api/users/<int:user_id>', methods = ['PUT']) #(update user 123, from data provided with the request)
@auth.login_required
def update_user(user_id):
   app.logger.debug('metodo put')
   user = User.query.filter_by(id = user_id).first_or_404()
   user.name = str(request.json.get('name', ''))
   user.email = str(request.json.get('email', ''))
   user.username = str(request.json.get('username', ''))
   user.password = user.hash_password(str(request.json.get('password', '')))
   db.session.commit()
   response = jsonify(user.serialize)
   response.status_code = 200
   return response


#http://localhost/api/users/123
@app.route('/api/users/<int:user_id>', methods = ['DELETE']) #(delete user 123, from data provided with the request)
@auth.login_required
def delete_user(user_id):
   user = User.query.filter_by(id = user_id).first_or_404()
   user.delete()
   response = jsonify({'message': 'User deleted successfully'})
   response.status_code = 204
   return response
