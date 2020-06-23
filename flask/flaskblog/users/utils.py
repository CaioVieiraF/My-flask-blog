import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_image(img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(img.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path,
        'static/profile_pics',
        picture_fn
    )

    output_size = (125, 125)
    i = Image.open(img)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        'Password reset request',
        sender='noreply@demo.com',
        recipients=[
            user.email
        ]
    )

    msg.body = f'''
To reset your password, visit the following link:
{url_for('users.request_token', token=token, _external=True)}
if you didn't make this request you can ignore this E-mail.
    '''
    mail.send(msg)


def send_delete_email(user):
    token = user.get_reset_token()
    msg = Message(
        'Account delete request',
        sender='noreply@demo.com',
        recipients=[
            user.email
        ]
    )

    msg.body = f'''
To delete your account, visit the following link:
{url_for('users.request_token_delete',
    user_id=user.id,
    token=token,
    _external=True
)}
if you didn't make this request you can ignore this E-mail.
    '''
    mail.send(msg)
