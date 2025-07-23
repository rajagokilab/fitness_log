from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class WorkoutForm(FlaskForm):
    workout_type = SelectField('Workout Type', choices=[('Walking', 'Walking'), ('Running', 'Running'), ('Cycling', 'Cycling'), ('Gym', 'Gym')], validators=[DataRequired()])
    steps = IntegerField('Steps', validators=[Optional()])
    hours = FloatField('Hours', validators=[Optional()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Log Workout')

class UpdateProfileForm(FlaskForm):
    username = StringField('New Username', validators=[DataRequired(), Length(min=3)])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[Length(min=8), Optional()])
    confirm_new_password = PasswordField('Confirm New Password', validators=[EqualTo('new_password'), Optional()])
    submit = SubmitField('Update Profile')
