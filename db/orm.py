from flask_sqlalchemy import SQLAlchemy
from db.entities import db
from db.init_db import load_initial_data

orm = db

def initialise(app):
    """
        Initialise the SQLAlchemy ORM.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/orm.sqlite'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"future":True}
    
    orm.init_app(app)

    # Create all tables.
    orm.create_all()

    # Insert the default values required for the application. This will be done on first startup.
    load_initial_data(app)

    return orm