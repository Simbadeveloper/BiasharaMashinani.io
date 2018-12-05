
#routes.py

"""
routes for the app
"""
#import from libraries
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm,BusinessForm
from app.models import User, Business
from flask_login import login_user, current_user, logout_user, login_required


#mock database for business
"""
businesses = [
    {
        'business': 'Andela',
        'title': 'ANDELA',
        'content': 'Excellent passion intergrity collaboration',
        'date_posted': 'April 20, 2018'
    },
    {
        'business': 'Google',
        'title': 'Google',
        'content': 'Second company ',
        'date_posted': 'April 21, 2018'
    },
    {
        'business': 'Udacity',
        'title': 'Udacity',
        'content': 'Third company ',
        'date_posted': 'April 21, 2018'
    },
]
"""
#route for home and index
@app.route("/")
@app.route("/businesses")
def home():
    """Home function for all business"""
    businesses = Business.query.all()
    return render_template('home.html', businesses=businesses)

#route for about
@app.route("/about")
def about():
    """about function for more details of the app_site"""
    return render_template('about.html', title='About')

#route for register
@app.route("/register", methods=['GET', 'POST'])
def register():
    """register functtion to dignup user"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    """login function for login a user after registering"""
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

#logout route
@app.route("/logout")
def logout():
    """logout function and redirect to home function"""
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    """function to save picture"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

#route account
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """account function to display informatin for user"""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

#route new_post
@app.route("/businesses/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """function for creating a new business"""
    form = BusinessForm()
    if form.validate_on_submit():
        business = Business(title=form.title.data, content=form.content.data, business=current_user)
        db.session.add(business)
        db.session.commit()
        flash('Your business has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Business',
                           form=form, legend='New Business')

#route
@app.route("/businesses/<int:post_id>")
def post(post_id):
    """function to post a new business"""
    business = Business.query.get_or_404(post_id)
    return render_template('post.html', title=business.title, business=business)


@app.route("/business/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """function to update a business"""
    business = Business.query.get_or_404(post_id)
    if business.business != current_user:
        abort(403)
    form = BusinessForm()
    if form.validate_on_submit():
        business.title = form.title.data
        business.content = form.content.data
        db.session.commit()
        flash('Your Business has been updated!', 'success')
        return redirect(url_for('post', post_id=business.id))
    elif request.method == 'GET':
        form.title.data = business.title
        form.content.data = business.content
    return render_template('create_post.html', title='Update Business',
                           form=form, legend='Update Business')


@app.route("/businesses/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """function for deleting a business by id"""
    business = Business.query.get_or_404(post_id)
    if business.business != current_user:
        abort(403)
    db.session.delete(business)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
