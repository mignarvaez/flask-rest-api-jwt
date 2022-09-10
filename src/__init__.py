# Application factory
# Create a flask application

# Any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned.
from flask import Flask

# For handling routes in the system directory
import os

# Import JWT library
from flask_jwt_extended import JWTManager
from src.constants.http_status_code import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

# Import blueprints
# it is necessary for files from folders use the full path, example: src.routes.auth 
from src.routes.auth import auth
from src.routes.prescriptions import prescriptions
from .database import db
# We import the models here in order to allow sqlalchemy to create all tables when start the application.
from src.models.patient import Patient
from src.models.prescription import Prescription

# Libraries required by swagger
from flasgger import Swagger, swag_from
from src.config.swagger import template,swagger_config

# Creater the app, it needs a text_config by default and you can set it as None
def create_app(test_config=None):
    # Create and configure the app
    # Name indicate the current python module
    # Instance relative config = True indicate that config files are relative to the instance folder, outside
    # package and hold local data that shouldn’t be committed to version control, such as configuration secrets and the database file.
    app = Flask(__name__,
                instance_relative_config=True)
    
    # Set default config, like a secret_key that will be used in order to keep data safe
    # Also, we import the JWT_SECRET_KEY
    # We get it from .env 
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
        
        SWAGGER = {
            'title':'Prescription API',
            'uiversion':3
        }
    )
    
    if test_config is None:
        # Load the instance config, if it exist, when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Registre db handler
    db.app=app
    db.init_app(app)
    db.create_all()
    
    # We implement JWTManager in app
    JWTManager(app)
    
    # Registre blueprints
    app.register_blueprint(auth)
    app.register_blueprint(prescriptions)
    
    # Set swagger
    Swagger(app, config=swagger_config, template=template)
    
    # Configure error handling for not found error
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return {'error':'not found'},HTTP_404_NOT_FOUND
    
    # Configure error handling for not found error
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return {'error':'Something went wrong, we are working on it'},HTTP_500_INTERNAL_SERVER_ERROR
    
    # Returns the app
    return app
    