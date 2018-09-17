from flask_login import UserMixin

from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    lastname = db.Column(db.String(30), nullable=False)
    firstname = db.Column(db.String(30), nullable=False)
    facility = db.Column(db.String(50), nullable=False)
    api_key = db.Column(db.String(50),nullable=False)

    def __init__(self,username, password, email,lastname,firstname,facility):
        self.username = username
        self.password = password
        self.email = email
        self.lastname = lastname
        self.firstname = firstname
        self.facility = facility

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.username)