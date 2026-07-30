# Habit Tracker

A web app for tracking daily habits and streaks. Built as a full-stack project with a real database and user accounts.

**Live demo:** https://habit-tracker-lqsw.onrender.com

## What it does

- Create an account and log in
- Add daily habits to track
- Check them off each day
- See your current streak for each habit

## Tech used

- Python, Flask — backend
- SQLAlchemy — database ORM
- Flask-Login — user authentication
- PostgreSQL — production database
- HTML, CSS — frontend
- Deployed on Render

## Run locally

1. Clone the repo and install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file:
   ```
   SECRET_KEY=your-secret-key
   ```

3. Run the app:
   ```
   python3 app.py
   ```

4. Open `http://127.0.0.1:5000`
