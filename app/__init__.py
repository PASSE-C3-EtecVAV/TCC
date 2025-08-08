from flask import Flask
from flask_mysqldb import MySQL
from config import Config
import boto3

class s3Handler:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.client = boto3.client(
            's3',
            aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=app.config['AWS_REGION']
        )

mysql = MySQL()
s3 = s3Handler()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mysql.init_app(app)
    s3.init_app(app)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    return app

