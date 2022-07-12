from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv



load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
import re

uri = os.getenv("DATABASE_URL")
# or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_DATABASE_URI'] = uri

db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)


from app import routes
