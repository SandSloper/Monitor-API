from flask_login import UserMixin
from app import db
# access roles
ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}

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
    business = db.Column(db.String(50),nullable=False)
    access = db.Column(db.Integer,nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self,username, password, email,lastname,firstname,facility,access,business,confirmed,confirmed_on=None):
        self.username = username
        self.password = password
        self.email = email
        self.lastname = lastname
        self.firstname = firstname
        self.facility = facility
        self.access = access
        self.business=business
        self.confirmed=confirmed
        self.confirmed_on=confirmed_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_admin(self):
        return self.access == ACCESS['admin']

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    #object to string
    def __repr__(self):
        return '<User %r>' % (self.username)