from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, UserForm
from app.models  import User
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/login', methods=["GET", "POST"])
def logMeIn():

    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    flash(f"Successfully logged in. Welcome back, {user.username}!", 'success')
                    login_user(user)
                    return redirect(url_for('homePage'))
                else:
                    flash("Incorrect password...", 'danger')
            else:
                flash("User does not exist...", 'danger')

    return render_template('login.html', form=form)

@auth.route('/signup', methods=["GET", "POST"])
def signUp():

    form = UserForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data

            u1 = User.query.filter_by(username=username).first()
            u2 = User.query.filter_by(email=email).first()

            if u1 and u2:
                flash('Username and email already exist', 'danger')
            elif u1:
                flash('Username already exists', 'danger')
            elif u2:
                flash('Email already exists', 'danger')
            else:
                user = User(username, first_name, last_name, email, password)
                user.saveToDB()

                flash('Succesfully created account!', 'success')

                return redirect(url_for('auth.logMeIn'))

    return render_template('signup.html', form=form)

@auth.route('/logout')
def logMeOut():
    logout_user()
    return redirect(url_for('homePage'))

@auth.route('/user')
@login_required
def viewUser():

    return render_template('user.html')

@auth.route('/user/<int:post_id>')
def viewUserInfo(user_id):
    # post = Post.query.filter_by(id = post_id).first()
    user = User.query.get(user_id)

    if user:
        return render_template('user.html', user=user)
    else:
        return redirect(url_for('auth.viewUserInfo'))

@auth.route('/user/<int:user_id>/update', methods=["GET", "POST"])
@login_required
def updateUser(user_id):
    user = User.query.get(user_id)
    if current_user.id != user.id:
        flash('You cannot update this user...', 'danger')
        return redirect(url_for('auth.viewUserInfo'))

    form = UserForm()

    if request.method == "POST":
        if form.validate():
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.password = password

            user.saveChanges()

            return redirect(url_for('auth.viewUserInfo', user_id=user_id))

    return render_template('update_user.html', form=form, user=user)

@auth.route('/posts/<int:user_id>/delete', methods=["GET"])
@login_required
def deleteUser(user_id):
    user = User.query.get(user_id)
    if current_user.id == user.id:
        logout_user()
        user.deleteFromDB()  
    else:
        flash('You cannot delete this post...', 'danger')
    return redirect(url_for('auth.logMeIn'))