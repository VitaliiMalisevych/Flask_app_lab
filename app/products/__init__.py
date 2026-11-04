import os
from flask import Blueprint
from tinydb import TinyDB

products_bp = Blueprint('products', __name__, template_folder='templates')

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'products.json')
db = TinyDB(db_path, encoding='utf-8')

from app.products import views