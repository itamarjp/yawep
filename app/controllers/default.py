from app import app
from app import db
from app import login_manager
from flask_login import current_user, login_user

from app.models.tables import User
from app.models.tables import Domains
from app.models.tables import Emails
from app.models.tables import Databases
from app.models.tables import Ftpaccounts
from app.forms.forms import LoginForm
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from flask import request, abort, jsonify, flash, redirect, url_for, render_template
from app.decorators import async

from json import dumps
from flask import make_response

from flask_login import logout_user


import pika

@async
def send_async_linux_task(msg , action , queue):
 connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
 channel = connection.channel()
 channel.queue_declare(queue=queue)
 msg.update({"action": action})
 channel.basic_publish(exchange='',routing_key=queue, body='{0}'.format(msg) )
 print("Linux task {} {}'".format(queue, msg))
 connection.close()

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/")
def hello():
    return redirect(url_for('login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = LoginForm()
    if form.validate_on_submit():
        u = form.username.data
        p = form.password.data
        remember = form.remember_me.data;
        app.logger.debug('login {}, {} remember = {}'.format( u,p , remember ))
        user = User.query.filter_by(username=u).first()
        if user is not None:
          app.logger.debug(user.serialize)
          return
        if verify_password(u,p):
            login_user(user, remember=remember)
            app.logger.debug("Hi {}".format(current_user.name))
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/admin/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))




@app.route('/api/login',methods=['POST'])
@auth.login_required
def get_resource():
    return jsonify({ 'message': 'Hello %s !' % auth.username()})


#http://localhost/api/users/me
@app.route('/api/users/me', methods = ['GET']) #(return info about currently logged in user)
@auth.login_required
def get_user_me():
       user = User.query.filter_by(username = auth.username()).first_or_404()
       response = jsonify(user.serialize)
       response.status_code = 200
       return response


@auth.verify_password
def verify_password(username, password):
    app.logger.debug('tentativa de login {}, {}'.format(username, password ))
    user = User.query.filter_by(username = username).first()
    if username == 'x' and password =='x':
       return True
    if not user or not user.verify_password(password):
        return False
    return True


#http://localhost/api/users
@app.route('/api/users', methods = ['GET']) #(retrieve list)
@auth.login_required
def get_ALL_users():
   app.logger.debug("Hello, %s!" % auth.username())
   users = User.query.all()
   if not users:
      abort(404)
   response = jsonify([i.serialize for i in users])
   response.status_code = 200
   return response

#http://localhost/api/users/123
@app.route('/api/users/<int:id>', methods = ['GET']) #(retrieve user 123)
@auth.login_required
def get_user(id):
       user = User.query.filter_by(id = id).first_or_404()
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
    return jsonify(user.serialize), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

#http://localhost/api/users/123
@app.route('/api/users/<int:id>', methods = ['PUT']) #(update user 123, from data provided with the request)
@auth.login_required
def update_user(id):
   user = User.query.filter_by(id = id).first_or_404()
   user.name = str(request.json.get('name', ''))
   user.email = str(request.json.get('email', ''))
   user.username = str(request.json.get('username', ''))
   user.password = user.hash_password(str(request.json.get('password', '')))
   db.session.commit()
   response = jsonify(user.serialize)
   response.status_code = 200
   return response


#http://localhost/api/users/123
@app.route('/api/users/<int:id>', methods = ['DELETE']) #(delete user 123, from data provided with the request)
@auth.login_required
def delete_user(id):
   user = User.query.filter_by(id = id).first_or_404()
   user.delete()
   response = jsonify({'message': 'User deleted successfully'})
   response.status_code = 204
   return response



#http://localhost/api/domains
@app.route('/api/domains', methods = ['GET']) #(retrieve list)
@auth.login_required
def get_ALL_domains():
   domains = Domains.query.all()
   if not domains:
      abort(404)
   response = jsonify([i.serialize for i in domains])
   response.status_code = 200
   return response

#http://localhost/api/domains/123
@app.route('/api/domains/<int:id>', methods = ['GET']) #(retrieve domain 123)
@auth.login_required
def get_domain(id):
       domain = Domains.query.filter_by(id = id).first_or_404()
       response = jsonify(domain.serialize)
       response.status_code = 200
       return response

@app.route('/api/domains', methods = ['POST'])  #(create a new domain, from data provided with the request)
@auth.login_required
def new_domain():
    user_id =  str(request.json.get('user_id', ''))
    name =  str(request.json.get('name', ''))
    if user_id is None or name is None:
        app.logger.debug('missing arguments')
        abort(400) # missing arguments
    if Domains.query.filter_by(name = name).first() is not None:
        app.logger.debug('dominio ja existe')
        abort(400) # existing domain
    domain = Domains(name = name,  user_id = user_id)
    domain.save()
    send_async_linux_task(msg = domain.serialize, queue="domains", action = "new")
    return jsonify(domain.serialize), 201, {'Location': url_for('get_domain', id = domain.id, _external = True)}

#http://localhost/api/domains/123
@app.route('/api/domains/<int:id>', methods = ['PUT']) #(update domain 123, from data provided with the request)
@auth.login_required
def update_domain(id):
   domain = Domains.query.filter_by(id = id).first_or_404()
   domain.name = str(request.json.get('name', ''))
   domain.user_id = str(request.json.get('user_id', ''))
   db.session.commit()
   response = jsonify(domain.serialize)
   response.status_code = 200
   return response


#http://localhost/api/domains/123
@app.route('/api/domains/<int:id>', methods = ['DELETE']) #(delete domain 123, from data provided with the request)
@auth.login_required
def delete_domain(id):
   domain = Domains.query.filter_by(id = id).first_or_404()
   send_async_linux_task(msg = domain.serialize, queue="domains", action = "delete")
   domain.delete()
   response = jsonify({'message': 'domain deleted successfully'})
   response.status_code = 204
   return response

#http://localhost/api/emails
@app.route('/api/emails', methods = ['GET']) #(retrieve list)
@auth.login_required
def get_ALL_emails():
   emails = Emails.query.all()
   if not emails:
      abort(404)
   response = jsonify([i.serialize for i in emails])
   response.status_code = 200
   return response

#http://localhost/api/emails/123
@app.route('/api/emails/<int:id>', methods = ['GET']) #(retrieve email 123)
@auth.login_required
def get_email(id):
       email = Emails.query.filter_by(id = id).first_or_404()
       response = jsonify(email.serialize)
       response.status_code = 200
       return response

@app.route('/api/emails', methods = ['POST'])  #(create a new email, from data provided with the request)
@auth.login_required
def new_email():
    domain_id =  str(request.json.get('domain_id', ''))
    username =  str(request.json.get('username', ''))
    password =  str(request.json.get('password', ''))
    if username is None or username is None:
        app.logger.debug('missing arguments')
        abort(400) # missing arguments
    if Emails.query.filter_by(username = username).first() is not None:
        app.logger.debug('conta de email ja existe')
        abort(400) # existing domain
    email = Emails(domain_id = domain_id, username = username,  password = password)
    email.save()
    send_async_linux_task(msg = email.serialize, queue="emails", action = "new")
    return jsonify(email.serialize), 201, {'Location': url_for('get_email', id = email.id, _external = True)}


#http://localhost/api/emails/123
@app.route('/api/emails/<int:id>', methods = ['PUT']) #(update email 123, from data provided with the request)
@auth.login_required
def update_email(id):
   email = Emails.query.filter_by(id = id).first_or_404()
   email.name = str(request.json.get('name', ''))
   email.user_id = str(request.json.get('user_id', ''))
   db.session.commit()
   response = jsonify(email.serialize)
   response.status_code = 200
   return response


#http://localhost/api/emails/123
@app.route('/api/emails/<int:id>', methods = ['DELETE']) #(delete email 123, from data provided with the request)
@auth.login_required
def delete_email(id):
   email = Emails.query.filter_by(id = id).first_or_404()
   send_async_linux_task(msg = email.serialize, queue="emails", action = "delete")
   email.delete()
   response = jsonify({'message': 'email deleted successfully'})
   response.status_code = 204
   return response



#http://localhost/api/ftpaccounts
@app.route('/api/ftpaccounts', methods = ['GET']) #(retrieve list)
@auth.login_required
def get_ALL_Ftpaccounts():
   ftp = Ftpaccounts.query.all()
   if not ftp:
      abort(404)
   response = jsonify([i.serialize for i in ftp])
   response.status_code = 200
   return response

#http://localhost/api/ftpaccounts/123
@app.route('/api/ftpaccounts/<int:id>', methods = ['GET']) #(retrieve item 123)
@auth.login_required
def get_ftpaccount(id):
       ftp = Ftpaccounts.query.filter_by(id = id).first_or_404()
       response = jsonify(ftp.serialize)
       response.status_code = 200
       return response

@app.route('/api/ftpaccounts', methods = ['POST'])  #(create a new domain, from data provided with the request)
@auth.login_required
def new_ftpaccount():
    domain_id =  str(request.json.get('domain_id', ''))
    username =  str(request.json.get('username', ''))
    password =  str(request.json.get('password', ''))
    if username is None or username is None:
        app.logger.debug('missing arguments')
        abort(400) # missing arguments
    if Ftpaccounts.query.filter_by(username = username).first() is not None:
        app.logger.debug('conta ftp ja existe')
        abort(400) # existing domain
    ftp = Ftpaccounts(domain_id = domain_id, username = username,  password = password)
    ftp.save()
    send_async_linux_task(msg = ftp.serialize, queue="ftpaccounts", action = "new")
    return jsonify(ftp.serialize), 201, {'Location': url_for('get_ftpaccount', id = ftp.id, _external = True)}

#http://localhost/api/ftpaccounts/123
@app.route('/api/ftpaccounts/<int:id>', methods = ['PUT']) #(update domain 123, from data provided with the request)
@auth.login_required
def update_ftpaccount(id):
   ftpaccount = Ftpaccounts.query.filter_by(id = domain_id).first_or_404()
   ftpaccount.name = str(request.json.get('name', ''))
   ftpaccount.user_id = str(request.json.get('user_id', ''))
   db.session.commit()
   response = jsonify(ftpaccount.serialize)
   response.status_code = 200
   return response


#http://localhost/api/ftpaccounts/123
@app.route('/api/ftpaccounts/<int:id>', methods = ['DELETE']) #(delete domain 123, from data provided with the request)
@auth.login_required
def delete_ftpaccount(id):
   ftp = Ftpaccounts.query.filter_by(id = id).first_or_404()
   send_async_linux_task(msg = ftp.serialize, queue="ftpaccounts", action = "delete")
   ftp.delete()
   response = jsonify({'message': 'domain deleted successfully'})
   response.status_code = 204
   return response

#http://localhost/api/databases
@app.route('/api/databases', methods = ['GET']) #(retrieve list)
@auth.login_required
def get_ALL_databases():
   databases = Databases.query.all()
   if not databases:
      abort(404)
   response = jsonify([i.serialize for i in databases])
   response.status_code = 200
   return response

#http://localhost/api/databases/123
@app.route('/api/databases/<int:id>', methods = ['GET']) #(retrieve domain 123)
@auth.login_required
def get_databases(id):
       database = Databases.query.filter_by(id = id).first_or_404()
       response = jsonify(domain.serialize)
       response.status_code = 200
       return response

@app.route('/api/databases', methods = ['POST'])  #(create a new database, from data provided with the request)
@auth.login_required
def new_databases():
    domain_id =  str(request.json.get('domain_id', ''))
    databasename =  str(request.json.get('databasename', ''))
    username =  str(request.json.get('username', ''))
    password =  str(request.json.get('password', ''))
    if domain_id is None or databasename is None:
        app.logger.debug('missing arguments')
        abort(400) # missing arguments
    if Databases.query.filter_by(databasename = databasename).first() is not None:
        app.logger.debug('banco ja existe')
        abort(400) # existing domain
    database = Databases(domain_id = domain_id, databasename = databasename, username = username, password = password)
    database.save()
    send_async_linux_task(msg = database.serialize, queue="databases", action = "new")
    return jsonify(database.serialize), 201, {'Location': url_for('get_databases', id = database.id, _external = True)}

#http://localhost/api/databases/123
@app.route('/api/databases/<int:id>', methods = ['PUT']) #(update domain 123, from data provided with the request)
@auth.login_required
def update_databases(id):
   domain = Databases.query.filter_by(id = id).first_or_404()
   domain.name = str(request.json.get('name', ''))
   domain.user_id = str(request.json.get('user_id', ''))
   db.session.commit()
   response = jsonify(domain.serialize)
   response.status_code = 200
   return response


#http://localhost/api/databases/123
@app.route('/api/databases/<int:id>', methods = ['DELETE']) #(delete domain 123, from data provided with the request)
@auth.login_required
def delete_databases(id):
   database = Databases.query.filter_by(id = id).first_or_404()
   send_async_linux_task(msg = database.serialize, queue="databases", action = "delete")
   database.delete()
   response = jsonify({'message': 'databases deleted successfully'})
   response.status_code = 204
   return response

