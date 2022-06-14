import os
import secrets
from PIL import Image, ImageOps
from flask import render_template, url_for, flash, redirect, request
from sssaves_app import app, db, bcrypt
from sssaves_app.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewSaveForm
from sssaves_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404'), 404

@app.route("/")
@app.route("/home")
def home():
	posts = Post.query.all()
	pfp = url_for('static', filename='pfp/' + current_user.pfp)
	return render_template('home.html', title='all', posts=posts, pfp=pfp)

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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))

def save_pfp(form_pfp):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_pfp.filename)
	pfp_filename = random_hex + f_ext
	pfp_path = os.path.join(app.root_path, 'static/pfp', pfp_filename)
	
	output_size = (320, 320)
	i = Image.open(form_pfp)
	i.thumbnail(output_size)
	i.save(pfp_path)

	return pfp_filename

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.new_pfp.data:
			pfp_file = save_pfp(form.new_pfp.data)
			current_user.pfp = pfp_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account information has been updated.', category='success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	pfp = url_for('static', filename='pfp/' + current_user.pfp)
	return render_template('account.html', title='my account', pfp=pfp, form=form)

@app.route("/profile")
@login_required
def profile():
	posts = Post.query.all()
	pfp = url_for('static', filename='pfp/' + current_user.pfp)
	return render_template('profile.html', title=current_user.username, pfp=pfp, posts=posts, profile=profile)

# @app.route('/profile/<username>')
# def profile(username):
#     profile = User.query.filter_by(username=username).first()
#     pfp = url_for('static', filename='pfp/' + current_user.pfp)
#     if profile is None:
#         return render_template('404.html')
#     else:
#         return render_template('profile.html', title=current_user.username, pfp=pfp, posts=posts, profile=profile)

@app.route("/save/new", methods=['GET', 'POST'])
@login_required
def new_save():
	form = NewSaveForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, url=form.url.data, category=form.category.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('You saved a thing!', category='success')
		return redirect(url_for('home'))
	pfp = url_for('static', filename='pfp/' + current_user.pfp)
	return render_template('create_save.html', title='new save', pfp=pfp, form=form)