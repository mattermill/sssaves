from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '56d96b331826e32177ffc6e6516ddf07'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from sssaves_app import routes