from app import db
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password_clear = db.Column(db.String)
    password_hash = db.Column(db.String(128))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)        

    def __init__(self, username, password,email):
        self.username = username
        self.password = password
        self.name = ''
        self.email = email
        self.password_clear = ''
        self.password_hash = self.hash_password(password)

    def __repr__(self):
        return "<User %r>" % self.username

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
