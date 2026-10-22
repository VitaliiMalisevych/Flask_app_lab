from flask import render_template, request, url_for, redirect
from . import user_bp

@user_bp.route('/hi/<string:name>')
def greetings(name):
    name_upper = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html", name=name_upper, age=age)

@user_bp.route('/admin')
def admin():
    to_url = url_for('users.greetings', name="administrator", age=45)
    return redirect(to_url)