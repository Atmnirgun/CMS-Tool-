"""This is a base class for database service. This class should be used by all entity service classes to
extend and make connection with DB."""

import os
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from utils import constants

def get_db():
    """ Helper method to create Sqlite DB connnection and configure it to return Row and return it. """
    
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """ Helper method to close the DB connection. """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """ Initialise the DB with required schema. """    
    
    db = get_db()

    #current_dir = os.path.dirname(os.path.abspath(__file__))
    #root_dir = os.path.dirname(current_dir)
    schema_file = 'config/schema.sql'#app_config.get(constants.CONFIG_PROP_DB_SCHEMA_FILE)
    with current_app.open_resource(schema_file) as f:
        db.executescript(f.read().decode('utf-8'))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """ This method configures the command init-db. This can be used to initialise the DB with required schema
    before starting the application. """
    click.echo("Initializing the DB!")
    init_db()
    click.echo("DB initialization complete!")


def init_app(app, app_config):
    """ This method registers the various method with application's lifecycle. """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)