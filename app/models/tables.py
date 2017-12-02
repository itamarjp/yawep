from app import db
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.inspection import inspect

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password_clear = db.Column(db.String)
    password_hash = db.Column(db.String(128))
    @property
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

        return {
           'id' : self.id ,
           'name' : self.name ,
           'email' :  self.email,
           'username' : self.username,
           'password_clear' : self.password_clear,
           'password_hash' : self.password_hash
           }

class Domain(db.Model):
    __tablename__ = "domains"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.Text)

class emails(db.Model):
    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'))
    username = db.Column(db.Text)
    password = db.Column(db.Text)

class ftpaccounts(db.Model):
    __tablename__ = "ftpaccounts"
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'))
    username = db.Column(db.Text)
    password = db.Column(db.Text)

class databases(db.Model):
    __tablename__ = "databases"
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'))
    databasename = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
