from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, URLField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sssaves_app.models import User
from bs4 import BeautifulSoup
import html, requests

# ---------------------------------------------#
#             New User Registration            #
# ---------------------------------------------#

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
		validators=[DataRequired(), Email()], render_kw={'placeholder': 'email'})

	password = PasswordField('Password', 
		validators=[DataRequired()], render_kw={'placeholder': 'password'})

	remember = BooleanField('Remember me')

	submit = SubmitField('Login')


# ---------------------------------------------#
#               ACCOUNT SETTINGS               #
# ---------------------------------------------#
class UpdateAccountForm(FlaskForm):

	username = StringField('Username',
		validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField('Email',
		validators=[DataRequired(), Email()])

	new_pfp = FileField('Update profile picture',
		validators = [FileAllowed(['jpg', 'png', 'gif'])])

	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username already exists. Please try again.')
	
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is already registered.')

# ---------------------------------------------#
#                 New Save                     #
# ---------------------------------------------#

# 1. Grab the title from a URL
# 2. Spit the title out so we can use it

class NewSaveForm(FlaskForm):
	title = StringField('Title', 
		validators=[DataRequired(), Length(min=2, max=200)], render_kw={'placeholder': 'Give it a name'})
	url = URLField('URL', validators=[DataRequired()], render_kw={'placeholder': 'e.g. zombo.com'})
	category = StringField('Category', default='uncategorized')
	submit = SubmitField('Save It')