from flask import render_template, request, redirect, url_for, flash, session, make_response
from . import user_bp

USERS_DATA = {
    "admin": "1234",
    "user1": "password"
}

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USERS_DATA and USERS_DATA[username] == password:
            session['username'] = username
            flash('Ви успішно увійшли в систему!', 'success')
            return redirect(url_for('users.profile'))
        else:
            flash('Wrong data! Try again!', 'danger')
            return redirect(url_for('users.login'))

    return render_template('users/login.html')

@user_bp.route('/profile')
def profile():
    if 'username' not in session:
        flash('Спочатку необхідно увійти в систему!', 'danger')
        return redirect(url_for('users.login'))

    username = session['username']
    cookies = request.cookies
    theme = request.cookies.get('theme', 'light')

    return render_template('users/profile.html', username=username, cookies=cookies, theme=theme)

@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@user_bp.route('/add_cookie', methods=['POST'])
def add_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))

    key = request.form.get('key')
    value = request.form.get('value')
    max_age = request.form.get('max_age')

    if key and value:
        response = make_response(redirect(url_for('users.profile')))
        max_age_val = int(max_age) if max_age and max_age.isdigit() else None
        response.set_cookie(key, value, max_age=max_age_val)
        flash(f'Кукі "{key}" успішно додано!', 'success')
        return response

    flash('Заповніть ключ та значення!', 'warning')
    return redirect(url_for('users.profile'))

@user_bp.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    if 'username' not in session:
        return redirect(url_for('users.login'))

    key = request.form.get('key')
    if key:
        response = make_response(redirect(url_for('users.profile')))
        response.delete_cookie(key)
        flash(f'Кукі "{key}" успішно видалено!', 'success')
        return response

    flash('Вкажіть ключ для видалення!', 'warning')
    return redirect(url_for('users.profile'))

@user_bp.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    if 'username' not in session:
        return redirect(url_for('users.login'))

    response = make_response(redirect(url_for('users.profile')))
    for key in request.cookies:
        if key != 'session':
            response.delete_cookie(key)

    flash('Усі користувацькі кукі успішно видалено!', 'success')
    return response

@user_bp.route('/change_theme/<theme_name>')
def change_theme(theme_name):
    if 'username' not in session:
        return redirect(url_for('users.login'))

    response = make_response(redirect(url_for('users.profile')))
    response.set_cookie('theme', theme_name, max_age=30*24*60*60)
    flash(f'Колірну схему змінено на "{theme_name}"!', 'info')
    return response