""" This module has been created to keep all page related routes together. It uses blueprints adds
/ as a context path. """
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from services.content_service import ContentService
from services.content_type_service import ContentTypeService
from services.auth_service import AuthService
from services.section_type_service import SectionTypeService
from services.section_service import SectionService
from services.user_service import UserService
from services.page_service import PageService
bp = Blueprint('pages', __name__)

# Register routes.
@bp.route("/")
def home_page():
    result = AuthService.is_logged_in()
    if result != True:
        return result
    page_service = PageService()
    user_service = UserService()
    user = user_service.get_user_by_username(username=session.get("username"))
    page_dtos = page_service.get_pages_by_user(user_id=user.id)
    return render_template("home.html", page=None, page_list=page_dtos)

@bp.route("/register")
def register():
    result = AuthService.is_logged_in()
    if result != True:
        return result
    return render_template("register.html")

@bp.route("/login",methods=["GET","POST"])
def login_page():
    if request.method == "POST":
        return redirect(url_for("pages.home_page"))
    else:
        return render_template("login.html")

@bp.route('/logout')
def logout():
    if session.get("username"):
        session.pop('username', None)
        return redirect(url_for('pages.login_page'))

@bp.route('/content')
def content():
    result = AuthService.is_logged_in()
    if result != True:
        return result
    error = None
    section_id = request.args.get("sectionId",None)
    page_id = request.args.get("pageId",None)
    content_type = ContentTypeService()   
    content_types = content_type.get_all()
    if section_id != None:
        section_service = SectionService()
        section_dto = section_service.get_section_by_id(section_id) 
        if section_dto == None:
            error = f"Requested  section with id {section_id} not found."
    else:
        error = f"Required property sectionId is missing."
        
    return render_template("content.html", section_id=section_id, content_types=content_types, error=error, page_id=page_id)

@bp.route('/content/<id>')  
def content_update(id):
    result = AuthService.is_logged_in()
    if result != True:
        return result
    section_id = request.args.get("sectionId",None)
    page_id = request.args.get("pageId",None)
    content_service = ContentService()
    content_type = ContentTypeService()
    content_dto = content_service.get_content_by_id(id=id)
    content_types = content_type.get_all()
    error = None
    if section_id != None:
        section_service = SectionService()
        section_dto = section_service.get_section_by_id(section_id) 
        if section_dto == None:
            error = f"Requested  section with id {section_id} not found."
    else:
        error = f"Required property sectionId is missing."
    
    return render_template("update_content.html", section_id=section_id, content_id=id, content=content_dto, content_types=content_types, error=error, page_id=page_id)

@bp.route('/content/delete/<id>')  
def delete_content(id):
    result = AuthService.is_logged_in()
    if result != True:
        return result
    section_id = request.args.get("sectionId",None)
    page_id = request.args.get("pageId",None)
    return render_template("delete_content.html",id=id, section_id=section_id, page_id=page_id)
    

@bp.route('/section')
def section():
    result = AuthService.is_logged_in()
    if result != True:
        return result
    page_id = request.args.get("pageId",None)
    section_type_service = SectionTypeService()    
    section_types = section_type_service.get_all()
    
    return render_template("section.html", section_id=None, section=None, section_types=section_types, error=None, page_id=page_id)

@bp.route('/section/<id>')  
def section_view(id):
    result = AuthService.is_logged_in()
    if result != True:
        return result

    section_service = SectionService()
    section_type = SectionTypeService()
    section_dto = section_service.get_section_by_id(id=id)
    error = None
    content_dtos = None
    section_types = None
    if section_dto != None:
        section_types = section_type.get_all()
        content_service = ContentService()
        content_dtos = content_service.get_content_by_section_id(sectionId=id)
    else:
        error = f"Section with id {id} not found."
    return render_template("section.html", section_id=id, section=section_dto, section_types=section_types, contents=content_dtos,error=error)

@bp.route('/section/edit/<id>')  
def section_update(id):
    result = AuthService.is_logged_in()
    if result != True:
        return result

    section_service = SectionService()
    section_type = SectionTypeService()
    section_dto = section_service.get_section_by_id(id=id)
    section_types = section_type.get_all()
    return render_template("update_section.html", section_id=id, section=section_dto, section_types=section_types)

@bp.route('/section/delete/<id>')  
def delete_section(id):
    page_id = request.args.get("pageId",None)
    return render_template("delete_section.html",id=id, page_id=page_id)

@bp.route('/page')
def create_page():
    result = AuthService.is_logged_in()
    if result != True:
        return result
    username = session.get("username",None)
    user_service = UserService()
    user = user_service.get_user_by_username(username=username)
    return render_template("page.html",userId = user.id)

@bp.route("/page/<id>")
def view_page(id):
    result = AuthService.is_logged_in()
    if result != True:
        return result
    page_service = PageService()
    user_service = UserService()
    page_dto = page_service.get_complete_page_by_id(page_id=id)
    user = user_service.get_user_by_username(username=session.get("username"))
    page_dtos = page_service.get_pages_by_user(user_id=user.id)
    print(page_dtos)
    return render_template("home.html", page=page_dto, page_list=page_dtos)

@bp.route('/page/edit/<id>')  
def page_update(id):
    result = AuthService.is_logged_in()
    if result != True:
        return result

    page_service = PageService()
    page_dto = page_service.get_page_by_id(page_id=id)
    return render_template("update_page.html",id=id, page=page_dto)

@bp.route('/page/delete/<id>')  
def delete_page(id):
    return render_template("delete_page.html",id=id)