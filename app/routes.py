from flask import make_response, render_template, url_for, redirect, request, flash
from app import app, bcrypt, db
from app.forms import RegistrationForm, LoginForm, CreatePostForm, UpdateAccountForm, SearchForm
from flask_login import current_user, login_required, login_user, logout_user
from app.models import City, Places, PostImage, User, Post, State, Country
from app.utils import save_picture, save_profile_picture




@app.route('/')
def index():
	page = request.args.get('page', 1, type=int)
	post_query = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
	return render_template('home.html', title='Home', post=post_query)


@app.route('/register', methods=['GET', 'POST'])
def reg():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(first_name=form.first_name.data,last_name=form.last_name.data, email=form.email.data,password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Successful')
		return redirect(url_for('login'))
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
		if form.profile_pic.data:
			picture_file = save_profile_picture(form.profile_pic.data)
			current_user.pic = picture_file
		current_user.first_name = form.first_name.data
		current_user.last_name = form.last_name.data
		current_user.email = form.email.data
		current_user.street = form.street.data
		if form.city.data and form.state.data and form.country.data:
			# city
			city_data = form.city.data.lower()
			city_query = City.query.filter(City.city_name.like(city_data)).first()
			if city_query:
				current_user.city = city_query.id
			else:
				city_data = form.city.data.lower()
				city = City(city_name=city_data)
				db.session.add(city)
				city_query = City.query.filter(City.city_name.like(city_data)).first()
				current_user.city = city_query.id
			# state
			state_data = form.state.data.lower()
			state_query = State.query.filter(State.state_name.like(state_data)).first()
			if state_query:
				current_user.state = state_query.id
			else:
				state_data = form.state.data.lower()
				state = State(state_name=state_data)
				db.session.add(state)
				state_query = State.query.filter(State.state_name.like(state_data)).first()
				current_user.state = state_query.id
			# country
			country_data = form.country.data.lower()
			country_query = Country.query.filter(Country.country_name.like(country_data)).first()
			if country_query:
				current_user.country = country_query.id
			else:
				country_data = form.country.data.lower()
				country = Country(country_name=country_data)
				db.session.add(country)
				db.session.flush()
				country_query = Country.query.filter(Country.country_name.like(country_data)).first()
				current_user.country = country_query.id
		db.session.commit()
		flash('Successful')
		return redirect(url_for('index'))
	# to fill up the form
	elif request.method == 'GET':
		form.first_name.data = current_user.first_name
		form.email.data = current_user.email
		form.last_name.data = current_user.last_name
		form.street.data = current_user.street
	return render_template('update_account.html', title='Update Account', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))



# remaining the tag feature to be done with this route
@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def create_post():
	form = CreatePostForm()
	if form.validate_on_submit():
		if form.location.data and form.city.data:
			location_data = form.location.data.lower()
			location_query = Places.query.filter(Places.name.like(location_data)).first()
			if location_query:
				post = Post(title=form.title.data, content=form.content.data, place= location_query.id, user_id=current_user.id)
				db.session.add(post)
				db.session.flush()
			else:
				city_data = form.city.data.lower()
				city_query = City.query.filter(City.city_name.like(city_data)).first()
				if city_query:
					location_data = form.location.data.lower()
					place = Places(name=location_data, city=city_query.id)
					db.session.add(place)
					db.session.flush()
					place_query = Places.query.filter(Places.name.like(location_data)).first()
					post = Post(title=form.title.data, content=form.content.data, place=place_query.id,user_id=current_user.id)
					db.session.add(post)
					db.session.flush()
				else:
					city_data = form.city.data.lower()
					city = City(city_name=city_data)
					db.session.add(city)
					db.session.flush()
					city_query = City.query.filter(City.city_name.like(city_data)).first()
					location_data = form.location.data.lower()
					place = Places(name=location_data, city=city_query.id)
					db.session.add(place)
					db.session.flush()
					place_query = Places.query.filter(Places.name.like(location_data)).first()
					post = Post(title=form.title.data, content=form.content.data, place=place_query.id, user_id=current_user.id)
					db.session.add(post)
					db.session.flush()
		else:
			post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
			db.session.add(post)
			db.session.flush()
		if form.image.data:
			for i in form.image.data:
				if i != None:
					picture_file = save_picture(i)
					image = PostImage(pic=picture_file, post_id=post.id)
					db.session.add(image)
				else:
					break
		db.session.commit()
		flash('Posted')
		return redirect(url_for('index'))
	return render_template('create_post.html',title='Create Post', form=form)




@app.route('/singlepost/<int:id>', methods=['GET', 'POST'])
def single_post(id):
	post = Post.query.get_or_404(id)
	images = db.session.query(PostImage).filter(PostImage.post_id == post.id).all()
	return render_template('post.html', title='Post', post=post, images=images)


@app.route('/singleuser/<int:id>', methods=['GET', 'POST'])
def single_user(id):
	user = User.query.get_or_404(id)
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).all()
	return render_template('user_account.html', title='Account', user=user, post=posts)


@app.context_processor
def layout():
	form= SearchForm()
	return dict(form=form)

@app.route('/search', methods=['POST'])
def search():
	page = request.args.get('page', 1, type=int)
	form = SearchForm()
	posts = Post.query
	if form.validate_on_submit():
		searched = form.searched.data
		posts = posts.filter(Post.content.like(f"%{searched}%") | Post.title.like(f"%{searched}%"))
		posts = posts.order_by(Post.title).paginate(page=page, per_page=3)
	return render_template('search.html', title='Search', form=form, searched=searched, posts=posts)

