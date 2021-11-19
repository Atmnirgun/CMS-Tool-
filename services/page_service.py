from db.entities import Page
from db.orm import db
from models.page_dto import PageDTO
from services.section_service import SectionService

class PageService():

    def create_page(self, page_dto:dict):
        page = Page(id = page_dto.id,
                name = page_dto.name,
                is_active = page_dto.is_active,
                user_id = page_dto.user_id,
                sections = page_dto.sections)

        db.session.add(page)
        db.session.commit()
        db.session.flush()
        return page.id
    
    def get_pages_by_user(self, user_id:int):
        print(user_id)
        pages = Page.query.filter_by(user_id=user_id).all()
        page_dtos = []
        if pages != None:
            for page in pages:
                page_dto = PageDTO(id=page.id, name=page.name, is_active=page.is_active, user_id=page.user_id, sections=page.sections)
                page_dtos.append(page_dto)
        return page_dtos

    def get_page_by_id(self, page_id:int):
        page = Page.query.filter_by(id=page_id).first()
        page_dto = None
        if page != None:
            page_dto = PageDTO(id=page.id, name=page.name, is_active=page.is_active, user_id=page.user_id, sections=page.sections)
        return page_dto

    def get_complete_page_by_id(self, page_id:int):
        page = Page.query.filter_by(id=page_id).first()
        page_dto = None
        if page != None:
            section_service = SectionService()
            sections = section_service.get_sections_by_page(page.id, full_details=True)
            page_dto = PageDTO(id=page.id,name=page.name, is_active=page.is_active, user_id=page.user_id, sections=sections)
        return page_dto
        
    def update_page(self, page_dto:PageDTO):
        page = Page.query.get(page_dto.id)

        if page != None:
            page.name = page_dto.name
            page.is_active = page_dto.is_active
            
            db.session.commit()
        else:
            raise Exception(f"Section with id {page_dto.id} not found.")

    def page_validation(self, page_data:dict):
            result = {}
            status = "error"
            error_msg = ""
            success_msg = ""
            data = None
            if page_data == None or not page_data:
                error_msg = "Something went wrong"
            else:
                page_name = page_data.get("page_name", None)
                    
                page_name_err = None
                has_error = False
                if page_name == None or not page_name:
                    page_name_err = "Please enter valid page name."
                    has_error = True
                if not has_error:
                    status = "success"
                    success_msg = "Page created successfully."
                
                data = {}
                if page_name_err != None:
                    data["page_name"] = page_name_err
            result['status'] = status
            if error_msg != None and error_msg:
                result['error_msg'] = error_msg
            if success_msg != None and success_msg:
                result['success_msg'] = success_msg
            if data != None:
                result['data'] = data
            
            return result

    def delete_page_by_id(self, page_id:int):
        page = Page.query.filter_by(id=page_id).first() 
        db.session.delete(page)
        db.session.commit()
