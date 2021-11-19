""" This module has been created to keep all REST API related routes toghter. It uses blueprints adds
/api as a context path. """
import functools
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from models.page_dto import PageDTO
from services.auth_service import AuthService
from validators import content_validator
from services.content_service import ContentService
from services.page_service import PageService
from services.section_type_service import SectionTypeService
from services.section_service import SectionService
from services.content_type_service import ContentTypeService
from services.user_service import UserService
from models.user_dto import UserDTO
from models.content_dto import ContentTypeDTO, ContentDTO
from models.section_dto import SectionDTO,SectionTypeDTO
bp = Blueprint('apis', __name__, url_prefix="/api")


@bp.route("/test", methods=["GET"])
def test():
    return jsonify({'Tested': 'Okay'})
    
@bp.route("/sectiontype", methods=["GET"])
def section_types():
    section_type_service = SectionTypeService()

    dtos = section_type_service.get_all()
    models = [ dto.__dict__ for dto in dtos]
    return jsonify(models)
    

@bp.route("/contenttype", methods=["GET"])
def content_types():
    con_type_service = ContentTypeService()

    dtos = con_type_service.get_all()
    models = [ dto.__dict__ for dto in dtos]
    return jsonify(models)

@bp.route("/authenticate",methods = ["POST"])
def auth():
    content = request.json
    return AuthService.auth_user(content)

@bp.route("/register",methods = ["POST"])
def create_user():
    user_data = request.json
    user_service = UserService()
    result = user_service.user_data_validation(user_data=user_data)
    
    status = result.get("status",None)
    if status == 'success':
        user_dto = UserDTO(id=None, user_name=user_data["user_name"], first_name=user_data["first_name"], last_name=user_data["last_name"], password=user_data["password"], email_id=user_data["email"],is_active=user_data["activate_check"])
        user_service.create_user(user_dto=user_dto)
        return result
    else:
        return result

@bp.route("/content",methods = ["POST"])
def content():
    content = request.json
    content_service = ContentService()
    content_type_service = ContentTypeService()
    result, section_dto = content_validator.content_validation(content=content)
    status = result.get("status",None)
    print(result)
    if status == 'success':
        content_type_id = int(content['content_type'])
        content_type_dto = content_type_service.get_by_id(content_type_id)
        content_dto = ContentDTO(id=None,name=content['content_name'],content_type=content_type_dto,section_id=section_dto.id,
                        is_active=content['activate_check'],data=content['contents'], section=section_dto)
        content_service.create_content(content_dto=content_dto)
        return result
    else:
        return result

@bp.route("/content/<id>",methods = ["PUT"])
def content_update(id):
    content = request.json
    
    content_service = ContentService()
    content_type_service = ContentTypeService()
    result,section_dto = content_validator.content_validation(content=content)
    print(result)
    status = result.get("status",None)
    if status == "success":
        content_type_id = int(content['content_type'])
        content_type = content_type_service.get_by_id(content_type_id)
        db_content = ContentDTO(id=id,name=content['content_name'],content_type=content_type,section_id=section_dto.id, is_active=content['activate_check'],data=content['contents'])
        content_service.update_content(db_content)

        result["success_msg"] = "Content Updated Seccessfully"
        return result
    else:
        return result

@bp.route("/content/delete/<id>", methods =['DELETE'])
def delete_content(id):
    msg = {}
    data = request.json
    content_service = ContentService()
    content = content_service.get_content_by_id(data["content_id"])
    if(content != None):
        content_service.delete_content_by_id(int(data["content_id"]))
        msg["success"] = "Content deleted successfully."
    else:
        msg["error"] = f"Content with id {id} not found."
    return msg

@bp.route("/section",methods = ["POST"])
def section():
    section = request.json
    section_service = SectionService()
    section_type_service = SectionTypeService()
    result = section_service.section_validation(section=section)
    print(result)
    status = result.get("status", None)
    if status == 'success':
        section_type_id = int(section['section_type'])
        section_type = section_type_service.get_by_id(section_type_id)
        section_dto = SectionDTO(id=None,name=section['section_name'], section_type=section_type, is_active=section['activate_check'], page_id=section["page_id"], contents=[])
        id = section_service.create_section(section_dto=section_dto)
        section['section_type'] = section_type.__dict__
        section['id'] = id
        result['data'] = section 
        return result
    else:
        return result

@bp.route("/section/<id>",methods = ["PUT"])
def section_update(id):
    section = request.json
    
    section_service = SectionService()
    section_type_service = SectionTypeService()
    result = section_service.section_validation(section=section)
    status = result.get("status",None)
    if status == "success":
        section_type_id = int(section['section_type'])
        section_type = section_type_service.get_by_id(section_type_id)
        section_db = SectionDTO(id=id,name=section['section_name'], section_type=section_type, is_active=section['activate_check'],page_id=None, contents=[])
        section_service.update_section(section_db)

        result["success_msg"] = "Section Updated Seccessfully"
        return result
    else:
        return result

@bp.route("/section/delete/<id>", methods =['DELETE'])
def delete_section(id):
    msg = {}
    data = request.json
    section_service = SectionService()
    section = section_service.get_section_by_id(data["section_id"])
    if(section != None):
        section_service.delete_section_by_id(int(data["section_id"]))
        msg["success"] = "Section deleted successfully."
    else:
        msg["error"] = f"Section with id {id} not found."
    return msg

@bp.route("/page", methods = ["POST"])
def create_page():
    page_data = request.json
    page_service = PageService()
    result = page_service.page_validation(page_data=page_data)
    print(page_data)
    status = result.get("status", None)
    if status == "success":
        page_dto = PageDTO(id=None, name=page_data["page_name"], is_active=page_data["activate_check"], user_id=page_data["user_id"], sections=[])
        page_id = page_service.create_page(page_dto)
        result["data"] = page_id
        return result
    else:
        return result  

@bp.route("/page/<id>",methods = ["PUT"])
def page_update(id):
    page_data = request.json
    
    page_service = PageService()
    result = page_service.page_validation(page_data=page_data)
    status = result.get("status",None)
    if status == "success":
        page_db = PageDTO(id=id,name=page_data['page_name'], is_active=page_data['activate_check'],user_id=None, sections=[])
        page_service.update_page(page_db)

        result["success_msg"] = "page Updated Seccessfully"
        return result
    else:
        return result

@bp.route("/page/delete/<id>", methods =['DELETE'])
def delete_page(id):
    msg = {}
    data = request.json
    page_service = PageService()
    page = page_service.get_page_by_id(data["page_id"])
    if(page != None):
        page_service.delete_page_by_id(int(data["page_id"]))
        msg["success"] = "Page deleted successfully."
    else:
        msg["error"] = f"Page with id {id} not found."
    return msg
