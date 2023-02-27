from flask import url_for
from flaskblog import app, mail
from PIL import Image
from flask_mail import Message
import secrets
import os

def save_picture(form_picture):
    # randomize the name of the picture
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex+f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resize the picture
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    # print("os.environ.get('EMAIL_USERNAME:", os.environ.get('EMAIL_USERNAME'))
    msg = Message("Password reset", sender=app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = repr(f'''To reset your password, please visit the following link:
                    {url_for("users.reset_token", token=token, _external=True )}  If you did not make this request, simply ignore this email and no change will be applied!
''')
    mail.send(msg)