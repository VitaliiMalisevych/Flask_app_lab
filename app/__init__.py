
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


app = Flask(__name__)
app.secret_key = 'super-secret-key-lab4'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lab7.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(model_class=Base)
db.init_app(app)

migrate = Migrate(app, db)

from . import views
from .users.views import user_bp
from app.products import products_bp
from app.products.models import Product, Category

app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(user_bp, url_prefix='/users')
