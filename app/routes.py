from app import app
from flask import render_template, flash, url_for, redirect
from flask_login import current_user
from .models import User

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')