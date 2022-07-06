import os
import secrets
from app import app

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fname = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/pic', picture_fname)
	form_picture.save(picture_path)
	return picture_fname
