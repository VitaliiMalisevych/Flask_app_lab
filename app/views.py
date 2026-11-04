import logging
from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import ContactForm

# Налаштування логування в файл
logging.basicConfig(
    filename='contacts.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    encoding='utf-8'
)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Формування та запис даних форми в log-файл
        log_data = f"Name: {form.name.data}, Email: {form.email.data}, Phone: {form.phone.data}, Subject: {form.subject.data}, Message: {form.message.data}"
        logging.info(log_data)

        flash('Ваше повідомлення успішно відправлено та записано в лог!', 'success')
        return redirect(url_for('contact'))  # PRG (Post/Redirect/Get)

    return render_template('contacts.html', form=form)