from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from models import db, User, Workout
from forms import RegisterForm, LoginForm, WorkoutForm, UpdateProfileForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fitnesssecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pw)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registered successfully!', 'success')
            return redirect(url_for('login'))
        except:
            flash('Username already exists.', 'danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Welcome {user.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(
            workout_type=form.workout_type.data,
            steps=form.steps.data,
            hours=form.hours.data,
            date=form.date.data,
            user_id=current_user.id
        )
        db.session.add(workout)
        db.session.commit()
        session['last_workout'] = form.workout_type.data  # save in session
        flash('Workout logged!', 'success')
        return redirect(url_for('dashboard'))

    last = session.get('last_workout', None)
    return render_template('dashboard.html', form=form, last_workout=last)

@app.route('/history')
@login_required
def history():
    workouts = Workout.query.filter_by(user_id=current_user.id).order_by(Workout.date.desc()).all()
    return render_template('history.html', workouts=workouts)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm(obj=current_user)
    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.current_password.data):
            current_user.username = form.username.data
            if form.new_password.data:
                current_user.password = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('Profile updated!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Current password incorrect.', 'danger')
    return render_template('profile.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
