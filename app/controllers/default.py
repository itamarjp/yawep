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

from sqlalchemy.inspection import inspect

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

@app.route('/api/xusers', methods = ['POST','GET'])
def xnew_user():
    form_user = NewUserForm()
    if form_user.validate_on_submit():
     username = request.json.get('username')
     password = request.json.get('password')
     if username is None or password is None:
         abort(400) # missing arguments
     if User.query.filter_by(username = username).first() is not None:
         abort(400) # existing user
     user = User(username = username)
     user.hash_password(password)
     db.session.add(user)
     db.session.commit()
    return render_template('newuser.html', form=form_user)



@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


#users api


def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'id':
            new_user['uri'] = url_for('get_user', user_id = user['id'], _external = True)
        else:
            new_user[field] = user[field]
    return new_user

#http://localhost/api/users
@app.route('/api/users', methods = ['GET']) #(retrieve list)
def get_ALL_users():
   users = User.query.all()
   #return jsonify({'users':users}), 201, {'Location': url_for('get_ALL_user', _external = True)}
   #return make_response(dumps(users))
   #return jsonify(dict(users))
   #result = [d.__dict__ for d in users]
   #return jsonify(users=result)
   #import json
   #return json.dumps((users))
   #return jsonify( { 'users': map(make_public_user, users) } )
   results = []
   for user in users:
      obj = {
        'id': user.id ,
        'name' : user.name ,
        'email' : user.email , 
        'username' : user.username ,
        'password_clear' : user.password_clear
      }
   results.append(obj)
   response = jsonify(results)
   response.status_code = 200
   return response

#http://localhost/api/users/123
@app.route('/api/users/<int:user_id>', methods = ['GET']) #(retrieve user 123)
def get_user(user_id):
       user = User.query.filter_by(id = user_id).first()
       if not user:
          # Raise an HTTPException with a 404 not found status code
          abort(404)

       results = []
       #for user in users:
       obj = {
           'id': user.id ,
           'name' : user.name ,
           'email' : user.email , 
           'username' : user.username ,
           'password_clear' : user.password_clear
       }
       results.append(obj)
       response = jsonify(results)
       response.status_code = 200
       return response

      # return jsonify(user), 201, {'Location': url_for('get_user', user_id = user.id, _external = True)}


@app.route('/api/users', methods = ['POST'])  #(create a new user, from data provided with the request)
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None or email is None:
        app.logger.debug('missing arguments')
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        app.logger.debug('usuario ja existe')
        abort(400) # existing user
    if User.query.filter_by(email = email).first() is not None:
        app.logger.debug('email ja existe')
        abort(400) # existing user registered with email
    user = User(username = username,password = password, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', user_id = user.id, _external = True)}

#http://localhost/api/users/123
@app.route('/api/users/<int:user_id>', methods = ['PUT']) #(update user 123, from data provided with the request)
def update_user(user_id):
   user = User.query.filter_by(id = user_id).first()
   if not user:
      # Raise an HTTPException with a 404 not found status code
      abort(404)
   user.name = str(request.json.get('name', ''))
   user.email = str(request.json.get('email', ''))
   user.username = str(request.json.get('username', ''))
   user.password_clear = str(request.json.get('password_clear', ''))
   db.session.commit()
   response = jsonify({
           'id': user.id ,
           'name' : user.name ,
           'email' : user.email , 
           'username' : user.username ,
           'password_clear' : user.password_clear
       }
            response.status_code = 200
            return response


#http://localhost/api/users/123
@app.route('/api/users/<int:user_id>', methods = ['DELETE']) #(delete user 123, from data provided with the request)
def delete_user(user_id):
   user = User.query.filter_by(id = user_id).first()
   if not user:
      #Raise an HTTPException with a 404 not found status code
      abort(404)
   user_id = user.id
   db.session.delete(user)
   db.session.commit()
   return { "message": "User {} deleted successfully".format(user_id)}, 200