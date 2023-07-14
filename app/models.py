from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(db.Model,UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return self.name
    

class service_provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(200))
    average_rating =  db.relationship('Rating', backref='rated_user', lazy=True) # New field for average rating
    # Other fields in the service provider model
    
   
    def __repr__(self):
        return self.name

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Numeric(precision=10, scale=2))
    service_provider_id = db.Column(db.Integer, db.ForeignKey('service_provider.id'))