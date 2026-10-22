from flask import Flask

app = Flask(__name__)

from . import views
from .users.views import user_bp
from .products.views import product_bp

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(product_bp, url_prefix='/products')