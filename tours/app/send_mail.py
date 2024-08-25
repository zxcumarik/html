from flask import url_for, render_template
from flask_mail import Message

from . import mail


def send_confirmation_email(user):
    token = user.get_token()
    print(token)
    message = Message(
        'Confirm your email',
        sender='noreply@example.com',
        recipients=[user.email],
    )
    # message.body = f'''To confirm your email visit the following link:
    # {url_for('confirm_email', token=token, _external=True)}
    # '''
    message.html = render_template('email_template.html', token=token)
    mail.send(message)


def send_reset_password_email(user):
    token = user.get_token()
    message = Message(
        'Reset your password',
        sender='noreply@example.com',
        recipients=[user.email],
    )
    message.body = f'''To reset your password visit the following link:
    {url_for('reset_password', token=token, _external=True)}
    '''
    mail.send(message)