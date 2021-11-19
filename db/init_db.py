from db.entities import db, SectionType, ContentType, User
from utils import constants
import os
import json

orm = db

def load_data_file(data_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    full_file_path = os.path.join(root_dir, data_file)

    json_data = []
    with open(full_file_path, 'r') as data:
        json_data = json.load(data)

    return json_data

def load_section_types(json_data):
    section_types = json_data.get(constants.DB_DATA_KEY_SECTION_TYPES)
    for section_type in section_types:
        if orm.session.get(SectionType, section_type['id']) == None:
            type_entity = SectionType(
                id=section_type['id'],
                name=section_type['name'],
                description=section_type['description']
            )
            orm.session.add(type_entity)

    orm.session.commit()

def load_content_types(json_data):
    content_types = json_data.get(constants.DB_DATA_KEY_CONTENT_TYPES)
    for content_type in content_types:
        if orm.session.get(ContentType, content_type['id']) == None:
            type_entity = ContentType(
                id=content_type['id'],
                name=content_type['name'],
                description=content_type['description']
            )
            orm.session.add(type_entity)

    orm.session.commit()

def load_users(json_data):
    users = json_data.get(constants.DB_DATA_KEY_CONTENT_SYSTEM_USERS)
    for user in users:
        if orm.session.get(User, user['id']) == None:
            user_data = User(
                id = user['id'],
                user_name = user['userName'],
                first_name = user['firstName'],
                last_name = user['lastName'],
                password = user["password"],
                email_id = user["emailId"]
            )
            orm.session.add(user_data)
    orm.session.commit()

def load_initial_data(app):
    APP_CONFIG = app.config[constants.APP_CONFIG_OBJ]

    data_file = APP_CONFIG.get(constants.CONFIG_PROP_DB_INIT_DATA_FILE, constants.DEFAULT_DB_INIT_DATA_FILE)

    # Read the JSON file.
    json_data = load_data_file(data_file)

    # Load section types.
    load_section_types(json_data)

    # Load content types.
    load_content_types(json_data)

    # Load default system users.
    load_users(json_data)

