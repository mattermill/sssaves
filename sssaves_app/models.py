from datetime import datetime
from sssaves_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	pfp = db.Column(db.String(20), nullable=False, default='default.png')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.id}, {self.username}', '{self.email}', '{self.pfp}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	url = db.Column(db.String(), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	category = db.Column(db.String(), nullable=False, default='uncategorized')
	date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f"Post('{self.title}', '{self.url}', '{self.category}', '{self.date_posted}')"