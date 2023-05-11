from flask import Flask, request

from autooed.api.experiment import exp_bp


def create_app():
    print(__name__)
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(exp_bp, url_prefix='/api')
    return app
