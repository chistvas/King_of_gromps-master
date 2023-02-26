from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your-email-address'
app.config['MAIL_PASSWORD'] = 'your-email-password'

class ContactForm(FlaskForm):
    webpage = StringField('Webpage', validators=[DataRequired()])
    problem = StringField('Problem', validators=[DataRequired()])
    submit_time = StringField('Datetime', validators=[DataRequired()])