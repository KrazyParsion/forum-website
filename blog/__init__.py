# Importing required functions 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .decorator import login_required
# Flask constructor 
app = Flask(__name__)
# app.secret_key = "dev-secret-key"
app.config["SECRET_KEY"] = "123456" 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
from blog import routes