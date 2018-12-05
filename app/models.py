#models.py
"""
models
"""
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """decorator login_manager"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):#class user
    """class User handle user details"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    businesses = db.relationship('Business', backref='business', lazy=True)

    def __repr__(self):
        """representation of user"""
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Business(db.Model):#class Business
    """class Business handles business details"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """represntation of business"""
        return f"Business('{self.title}', '{self.date_posted}')"
