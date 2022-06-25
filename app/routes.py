from flask import render_template, url_for, redirect, request, flash
from app import app, bcrypt, db
from app.forms import RegistrationForm, LoginForm, CreatePostForm, UpdateAccountForm
from flask_login import current_user, login_required, login_user, logout_user
from app.models import City, Places, PostImage, User, Post


@app.route('/')
def index():
    return render_template('home.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def reg():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(first_name=form.first_name.data,last_name=form.last_name.data, email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Successful')
		return redirect(url_for('index'))
	return render_template('reg.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if current_user.is_authenticated:
			return redirect(url_for('index'))
		user = User.query.filter_by(email= form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user=user, remember=form.remember_me.data)
			flash('Good job', 'success')
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('index'))
		else:
			flash('Access Denied', "danger")
	return render_template('login.html',title='Login', form=form)



@app.route('/updateaccount', methods=['GET', 'POST'])
@login_required
def update_account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		current_user.email = form.email.data
		# to add the logic for updating address
		db.session.commit()
		flash('Successful')
		return redirect(url_for('index'))
	return render_template('reg.html', title='Register', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def create_post():
	form = CreatePostForm()
	if form.validate_on_submit():
		if form.location.data and form.city.data:
			location_query = Places.query.filter(Places.name.like(form.location.data)).first()
			if location_query:
				post = Post(title=form.title.data, content=form.content.data, place= location_query.id, user_id=current_user.id)
				db.session.add(post)
			else:
				city_query = City.query.filter(City.city_name.like(form.city.data)).first()
				if city_query:
					place = Places(name= form.location.data, city=city_query.id)
					db.session.add(place)
					place_query = Places.query.filter(Places.name.like(form.location.data)).first()
					post = Post(title=form.title.data, content=form.content.data, place=place_query.id,user_id=current_user.id)
					db.session.add(post)
				else:
					city = City(city_name=form.city.data)
					db.session.add(city)
					city_query = City.query.filter(City.city_name.like(form.city.data)).first()
					place = Places(name=form.location.data, city=city_query.id)
					db.session.add(place)
					place_query = Places.query.filter(Places.name.like(form.location.data)).first()
					post = Post(title=form.title.data, content=form.content.data, place=place_query.id, user_id=current_user.id)
					db.session.add(post)
		else:
			post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
			db.session.add(post)
		db.session.commit()
		flash('Posted')
		return redirect(url_for('index'))
	return render_template('create_post.html',title='Create Post', form=form)


@app.route('/singlepost', methods=['GET', 'POST'])
def single_post():
    return "<h1>Howdy</h1>"



@app.route('/search', methods=['GET', 'POST'])
def search():
    return "<h1>Howdy</h1>"