from flask import Flask, render_template
import os
from routes import api_routes, page_routes
from configparser import ConfigParser
from utils import constants
#from services import db_service
from db import orm


def create_app():
    """ Create and configure the Flask app. """

    # Read application settings.
    config = ConfigParser()
    config.read('config/app_config.ini')
    APP_CONFIG = config[constants.CONFIG_SECTION_APP_CONFIG]
    db_file = APP_CONFIG.get(constants.CONFIG_PROP_DB_FILE)
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        #DATABASE=os.path.join(app.instance_path, db_file),
    )

    # Store the app configuration into flask app.
    app.config[constants.APP_CONFIG_OBJ] = APP_CONFIG

    
    # Register the DB.
    #db_service.init_app(app, APP_CONFIG)

    # Register the ORM and initialise DB.
    with app.app_context():
        db = orm.initialise(app)

    # Register blueprints.
    app.register_blueprint(api_routes.bp) # All /api urls.

    app.register_blueprint(page_routes.bp) # All / urls except /api.
    app.add_url_rule('/', endpoint='index')
    
    return app
