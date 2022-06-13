from flask import render_template, url_for, flash, redirect
from sssaves_app import app, db, bcrypt
from sssaves_app.forms import RegistrationForm, LoginForm
from sssaves_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		form = RegistrationForm()
		if form.validate_on_submit():
			hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			user = User(username=form.username.data, email=form.email.data, password=hashed_password)
			db.session.add(user)
			db.session.commit()
			flash(f'Account created for {form.username.data}!', 'success')
			return redirect(url_for('login'))
		return render_template('register.html', title='register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))