import logging
from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import ContactForm

logging.basicConfig(
    filename='contacts.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    encoding='utf-8'
)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        log_data = f"Name: {form.name.data}, Email: {form.email.data}, Phone: {form.phone.data}, Subject: {form.subject.data}, Message: {form.message.data}"
        logging.info(log_data)

        flash('Ваше повідомлення успішно відправлено та записано в лог!', 'success')
        return redirect(url_for('contact'))

    return render_template('contacts.html', form=form)