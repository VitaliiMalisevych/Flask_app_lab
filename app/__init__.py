from flask import Flask

app = Flask(__name__)
app.secret_key = 'super-secret-key-lab4'

from . import views
from .users.views import user_bp
from app.products import products_bp


app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(user_bp, url_prefix='/users')
