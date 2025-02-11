from flask import Flask
from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.models import db


def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pass.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    @app.route('/')
    def home():
        return render_template('frontpage.html')
    
    return app