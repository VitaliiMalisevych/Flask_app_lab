
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='development'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.views import main_bp
    from app.users import user_bp
    from app.products import products_bp
    from app.posts import post_bp
    from app.posts import models

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(post_bp, url_prefix='/post')

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app
