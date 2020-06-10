from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class InviteUserForm(FlaskForm):
    email = StringField('New user email', validators=[DataRequired(), Email()])
    submit = SubmitField('Invite')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if (user is not None) and (user.username):
            raise ValidationError('Email already registered.')
        elif (user is not None):
            raise ValidationError('User already invited. Resending invite email.')

class ManageUserForm(FlaskForm):
    action_ = SelectField('Action', 
                          choices=[('del', 'Delete'),
                                   ('adm', 'Make admin')],
                          validate_choice=False)
    action2_ = SelectField('Action',
                           choices=[('del', 'Delete'),
                                    ('rma', 'Remove admin')],
                           validate_choice=False)
    user_ = HiddenField('user_')
    submit_ = SubmitField('>')
