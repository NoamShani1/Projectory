from flask import Flask
from flask import Blueprint, render_template


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('frontpage.html')

    return app