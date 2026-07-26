from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    habits = db.relationship('Habit', backref='user', lazy = True)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created = db.Column(db.Date, default=date.today)
    userid = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)
    completions = db.relationship('Completion', backref='habit', lazy=True)

class Completion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habitid = db.Column(db.Integer, db.ForeignKey('habit_id'), nullable=False)
    date = db.Column(db.Date, default=date.today)