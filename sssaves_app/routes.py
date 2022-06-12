from flask import render_template, url_for, flash, redirect
from sssaves_app import app
from sssaves_app.forms import RegistrationForm, LoginForm
from sssaves_app.models import User, Post

posts = [
	{
		'author': 'Matt Miller',
		'title': 'save 1',
		'content': 'twitter.com',
		'date_posted': 'june 10'
	},
	{
		'author': 'Snide Delch',
		'title': 'save 1',
		'content': 'twitter.com',
		'date_posted': 'june 10'
	},
	{
		'author': 'Randy Andes',
		'title': 'save 3',
		'content': 'randysforkliftrepair.com',
		'date_posted': 'june 8'
	}
]

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404'), 404

@app.route("/")
@app.route("/home")
def home():
		return render_template('home.html', title='home', posts=posts)

@app.route("/about")
def about():
		return render_template('about.html', title='about')

@app.route("/register", methods=['GET', 'POST'])
def register():
		form = RegistrationForm()
		if form.validate_on_submit():
			flash(f'Account created for {form.username.data}!', 'success')
			return redirect(url_for('home'))
		return render_template('register.html', title='register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
		form = LoginForm()
		if form.validate_on_submit():
			if form.email.data == 'admin@sssaves.com' and form.password.data == 'boop':
				flash(f'Welcome back!', 'success')
				return redirect(url_for('home'))
			else:
				flash(f'Login unsuccessful', 'error')
		return render_template('login.html', title='login', form=form)
