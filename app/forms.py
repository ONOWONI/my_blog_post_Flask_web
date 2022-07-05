from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, BooleanField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app.models import City, User, Places
from flask_login import current_user


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=4)])
    confirm_password = PasswordField('Confirm Pasword', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Invalid Email')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')




class CreatePostForm(FlaskForm):
    title = StringField('Title')
    content = TextAreaField('Post', validators=[DataRequired() ])
    image = FieldList(FileField("Add Images", validators=[FileAllowed(['jpg', 'png'])]), min_entries=5)
    location = StringField("Location")
    city = StringField("City")
    tags = StringField("Tags")
    submit = SubmitField('Upload')



class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    country = StringField('Country')
    street = StringField('House address')
    city = StringField('City')
    state = StringField('State')
    profile_pic = FileField("Add a Profile Pic", validators=[FileAllowed(['jpg', 'png', 'gif'])])
    submit = SubmitField('Update')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Invalid Email')


