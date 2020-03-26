import os
from flask import Flask, render_template, url_for, redirect, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_mail import Mail, Message


app = Flask(__name__)

app.config.update(
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string'),
    MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER = ('Beck Zhai', os.getenv('MAIL_USERNAME'))
)

mail = Mail(app)


#SMTP
def send_smtp_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)



class EmailForm(FlaskForm):
    to = StringField('To', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit_smtp = SubmitField('Send with SMTP')




class SubscribeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')



@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if form.validate_on_submit():
        to = form.to.data
        subject = form.subject.data
        body = form.body.data
        if form.submit_smtp.data:
            send_smtp_mail(subject, to, body)
        #     method = request.form.get('sumbit_smtp')
        # flash('Email sent %s! Check your inbox.' % ' '.join(method.split()))
        flash('Email sent success! Check your inbox.')
        return redirect(url_for('index'))
    form.subject.data = 'Hello, World!'
    form.body.data = 'Across the Great Wall we can reach every corner in the world.'
    return render_template('index.html', form=form)



@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        flash('Welcome on board!')
        send_smtp_mail('Subscribe Success!', email, 'Hello, thank you for subscribed!')
        return redirect(url_for('subscribe'))
    return render_template('subscribe.html', form=form)




# @app.route('/subscribe', methods=['GET', 'POST'])
# def subscribe():
#     form = SubscribeForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         email = form.email.data
#         send_smtp_mail('Subscribe Success!', email, name=name)
#         flash('Confirmation email have been sent! Check your inbox.')
#         return redirect(url_for('subscribe'))
#     return render_template()
