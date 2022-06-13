from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sssaves_app.models import User
import html

# ---------------------------------------------#
#             New User Registration            #
# ---------------------------------------------#

s = '<a href="/login" class="link link__primary">Sign in</a>'
login_link = html.escape(s)

class RegistrationForm(FlaskForm):

	username = StringField('Username',
		validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField('Email',
		validators=[DataRequired(), Email()])

	password = PasswordField('Password', 
		validators=[DataRequired()])

	confirm_password = PasswordField('Confirm Password', 
		validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username already exists. Please try again.')
	
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('That email is already registered.')

# ---------------------------------------------#
#                 User Login                   #
# ---------------------------------------------#

class LoginForm(FlaskForm):

	email = StringField('Email',
		validators=[DataRequired(), Email()])

	password = PasswordField('Password', 
		validators=[DataRequired()])

	remember = BooleanField('Remember me')

	submit = SubmitField('Login')