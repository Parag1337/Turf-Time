from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, FloatField, DateField, TimeField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from database.models import User
from datetime import date, datetime, time

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Account Type', choices=[('user', 'User'), ('owner', 'Turf Owner')], validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

class TurfForm(FlaskForm):
    name = StringField('Turf Name', validators=[DataRequired(), Length(min=3, max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(min=3, max=255)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price_per_hour = FloatField('Price per Hour (₹)', validators=[DataRequired()])
    image = FileField('Upload Image')
    submit = SubmitField('Add Turf')

class BookingForm(FlaskForm):
    booking_date = DateField('Booking Date', validators=[DataRequired()], format='%Y-%m-%d')
    start_time = TimeField('Start Time', validators=[DataRequired()], format='%H:%M')
    end_time = TimeField('End Time', validators=[DataRequired()], format='%H:%M')
    
    # Player finding fields
    public_booking = BooleanField('Make this booking public for team finding')
    max_players = SelectField('Maximum number of players', choices=[
        (0, 'No limit'), (2, '2'), (4, '4'), (6, '6'), (8, '8'), (10, '10'), (12, '12')
    ], coerce=int)
    notes = TextAreaField('Notes for other players (e.g., skill level, game type)')
    
    submit = SubmitField('Confirm Booking')
    
    def validate_booking_date(self, booking_date):
        if booking_date.data < date.today():
            raise ValidationError('Booking date cannot be in the past.')
    
    def validate_end_time(self, end_time):
        if self.start_time.data >= end_time.data:
            raise ValidationError('End time must be after start time.')

class FilterBookingsForm(FlaskForm):
    turf = SelectField('Turf', choices=[], validators=[])  # Choices will be filled dynamically
    status = SelectField('Status', choices=[
        ('all', 'All Statuses'), 
        ('confirmed', 'Confirmed'), 
        ('completed', 'Completed'), 
        ('cancelled', 'Cancelled')
    ])
    date_from = DateField('From Date', format='%Y-%m-%d', validators=[])
    date_to = DateField('To Date', format='%Y-%m-%d', validators=[])
    submit = SubmitField('Filter')

class TeamRequestForm(FlaskForm):
    message = TextAreaField('Message (Introduce yourself, mention your skill level, etc.)', validators=[DataRequired()])
    submit = SubmitField('Send Request')
