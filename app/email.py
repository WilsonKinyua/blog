from flask_mail import Message
from flask import render_template
from . import mail


def send_email(subject,template,to,**kwargs):
    sender_email = 'wilsonkinyuam@gmail.com'

    msg = Message(subject, sender=sender_email, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
