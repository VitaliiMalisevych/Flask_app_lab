from flask import render_template, request, redirect, url_for, flash, make_response
from flask_login import login_user, logout_user, current_user, login_required

from app import db
from app.users import user_bp
from app.users.forms import RegistrationForm, LoginForm
from app.users.models import User


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Реєстрація успішна! Тепер увійдіть у систему.', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', form=form)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Ви успішно увійшли!', 'success')
            return redirect(url_for('users.account'))
        flash('Неправильна електронна адреса або пароль.', 'danger')
    return render_template('users/login.html', form=form)


@user_bp.route('/account')
@login_required
def account():
    return render_template('users/account.html', user=current_user)


@user_bp.route('/list')
@login_required
def users_list():
    users = db.session.scalars(db.select(User).order_by(User.id)).all()
    return render_template('users/list.html', users=users)


@user_bp.route('/profile')
@login_required
def profile():
    return render_template(
        'users/profile.html',
        username=current_user.username,
        cookies=request.cookies,
        theme=request.cookies.get('theme', 'light')
    )


@user_bp.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))


@user_bp.route('/add_cookie', methods=['POST'])
@login_required
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    max_age = request.form.get('max_age')
    if key and value and key != 'session':
        response = make_response(redirect(url_for('users.profile')))
        max_age_val = int(max_age) if max_age and max_age.isdigit() else None
        response.set_cookie(key, value, max_age=max_age_val)
        flash(f'Кукі "{key}" успішно додано!', 'success')
        return response
    flash('Заповніть ключ та значення!', 'warning')
    return redirect(url_for('users.profile'))


@user_bp.route('/delete_cookie', methods=['POST'])
@login_required
def delete_cookie():
    key = request.form.get('key')
    if key and key != 'session':
        response = make_response(redirect(url_for('users.profile')))
        response.delete_cookie(key)
        flash(f'Кукі "{key}" успішно видалено!', 'success')
        return response
    flash('Вкажіть ключ для видалення!', 'warning')
    return redirect(url_for('users.profile'))


@user_bp.route('/delete_all_cookies', methods=['POST'])
@login_required
def delete_all_cookies():
    response = make_response(redirect(url_for('users.profile')))
    for key in request.cookies:
        if key not in ('session', 'remember_token'):
            response.delete_cookie(key)
    flash('Усі користувацькі кукі успішно видалено!', 'success')
    return response


@user_bp.route('/change_theme/<theme_name>')
@login_required
def change_theme(theme_name):
    if theme_name not in ('light', 'dark'):
        return redirect(url_for('users.profile'))
    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)
    flash(f'Колірну схему змінено на "{theme_name}"!', 'info')
    return response
