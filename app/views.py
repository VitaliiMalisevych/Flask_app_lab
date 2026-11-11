
import logging

from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import ContactForm

main_bp = Blueprint('main', __name__)

logging.basicConfig(
    filename='contacts.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    encoding='utf-8'
)


@main_bp.route('/')
def home():
    return render_template('homepage.html')


@main_bp.route('/resume')
def resume():
    return render_template('resume.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        log_data = (
            f"Name: {form.name.data}, "
            f"Email: {form.email.data}, "
            f"Phone: {form.phone.data}, "
            f"Subject: {form.subject.data}, "
            f"Message: {form.message.data}"
        )

        logging.info(log_data)

        flash(
            'Ваше повідомлення успішно відправлено та записано в лог!',
            'success'
        )

        return redirect(url_for('main.contact'))

    return render_template('contacts.html', form=form)
