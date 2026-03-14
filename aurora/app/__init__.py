"""
Aurora Price Comparison - Flask Application Factory
"""
from flask import Flask
import os

from app.extensions import db, login_manager, bcrypt


def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'aurora-secret-key-2024')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
        f'sqlite:///{os.path.join(basedir, "..", "instance", "aurora.db")}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Login configuration
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'
    
    # Import ALL models after db is initialized
    from app.models import (
        Category, Store, Product, Price, PriceHistory,
        User, Favorite, PriceAlert, Click, PageView
    )
    
    # Register blueprints
    from app.routes.main import main as main_blueprint
    from app.routes.auth import auth as auth_blueprint
    from app.routes.api import api as api_blueprint
    from app.routes.admin import admin as admin_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    # Create database tables (AFTER importing models)
    with app.app_context():
        db.create_all()
    
    return app


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
