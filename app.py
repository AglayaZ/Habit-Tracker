from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Habit, Completion
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///habits.db')

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(email=email).first():
            flash('An account with that email already exists')
            return redirect(url_for('signup'))
        if User.query.filter_by(username=username).first():
            flash('That username is already taken')
            return redirect(url_for('signup'))
        
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password")
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    today = date.today()
    habit_data = []

    for habit in habits:
        completions = [c.date for c in habit.completions]
        completed_today = today in completions
        streak = 0
        check_date = today

        while check_date in completions:
            streak += 1
            check_date = check_date.replace(day=check_date.day - 1)

        habit_data.append({
            'habit': habit,
            'completed_today': completed_today,
            'streak': streak
        })
    habit_data.sort(key=lambda x: x['completed_today'])
    return render_template('dashboard.html', habit_data=habit_data, today=today)

@app.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        habit = Habit(name=name, category=category, user_id=current_user.id)
        db.session.add(habit)
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    return render_template('addhabit.html')

@app.route('/complete/<int:habit_id>')
@login_required
def complete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    today = date.today()
    already_done = Completion.query.filter_by(habit_id=habit_id, date=today).first()

    if not already_done:
        completion = Completion(habit_id=habit_id, date=today)
        db.session.add(completion)
        db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/delete/<int:habit_id>')
@login_required
def delete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    Completion.query.filter_by(habit_id=habit_id).delete()
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)