from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message="Довжина ім'я має бути від 4 до 10 символів")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Email(message="Введіть коректну електронну пошту")
    ])
    phone = StringField('Phone', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Regexp(r'^\+380\d{9}$', message="Формат телефону: +380XXXXXXXXX")
    ])
    subject = SelectField('Subject', choices=[
        ('general', 'Загальне питання'),
        ('support', 'Технічна підтримка'),
        ('cooperation', 'Співпраця')
    ], validators=[DataRequired(message="Оберіть тему")])

    message = TextAreaField('Message', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(max=500, message="Довжина не більше 500 символів")
    ])
    submit = SubmitField('Send Message')