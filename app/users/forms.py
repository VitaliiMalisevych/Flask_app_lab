from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from app import db
from app.users.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Ім’я користувача', validators=[DataRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Підтвердження пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зареєструватися')

    def validate_username(self, field):
        if db.session.scalar(db.select(User).where(User.username == field.data)):
            raise ValidationError('Таке ім’я користувача вже існує.')

    def validate_email(self, field):
        if db.session.scalar(db.select(User).where(User.email == field.data)):
            raise ValidationError('Ця електронна адреса вже зареєстрована.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запам’ятати мене')
    submit = SubmitField('Увійти')
