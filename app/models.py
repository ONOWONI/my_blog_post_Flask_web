from app import login_manager, db
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(70), nullable=False)
    street = db.Column(db.String(255), nullable=False, default='none')
    city = db.Column(db.Integer,nullable=False, default=0)
    state = db.Column(db.Integer,nullable=False, default=0)
    country = db.Column(db.Integer,nullable=False, default=0)
    pic = db.Column(db.String(), nullable=False, default='default.png')
    date_created = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('PostComment', backref='commenter', lazy=True)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.UnicodeText())
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    place = db.Column(db.Integer, db.ForeignKey('places.id'))
    posts = db.relationship('PostImage', backref='picpost', lazy=True)

    def __repr__(self):
        return f"{self.title} - {self.content}"



class Places(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.Integer, db.ForeignKey('city.id'))
    posts = db.relationship('Post', backref='postlocation', lazy=True)

class PostImage(db.Model):
    __tablename__ = 'postimage'
    id = db.Column(db.Integer, primary_key=True)
    pic = db.Column(db.String(), nullable=False, default='default.png')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)



class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(), nullable=False, default='default')
    state = db.Column(db.Integer, nullable=False, default=0)


class State(db.Model):
    __tablename__ = 'State'
    id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(), nullable=False, default='default')
    country = db.Column(db.Integer, nullable=False, default=0)


class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(), nullable=False, default='default')



class PostComment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.UnicodeText())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

