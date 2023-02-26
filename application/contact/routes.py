from flask import Blueprint, current_app
from datetime import datetime
from flask import url_for, flash, redirect, request
from application import db, mail
from application.contact.models import Contact
from flask_mail import Message


contact_me = Blueprint('contact_me', __name__)

@contact_me.route("/contact", methods=['GET', 'POST'])
def contact():
    text = request.form.get('description')
    contact = Contact(
        webpage=request.full_path,
        description=request.form.get('description'),
        submit_time=datetime.utcnow()
        )
    db.session.add(contact)
    db.session.commit()
    recipient = 'king1of1gromps@gmail.com'
    sender = 'velx.l2@mail.ru'
    subject = 'New contact!'
    body = text

    msg = Message(subject=subject, body=body, sender=sender, recipients=[recipient])
    mail.send(msg)

    flash('Your message has been sent', "success")
    return redirect(url_for("search_engine.search"))