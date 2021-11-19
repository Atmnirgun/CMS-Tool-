from db.entities import Section,SectionType
from db.orm import db

from models.section_dto import SectionDTO, SectionTypeDTO
from services.content_service import ContentService

class SectionService():

    def create_section(self, section_dto:SectionDTO):
        section_type = section_dto.section_type
                
        section = Section(id=section_dto.id, 
            name=section_dto.name,  
            is_active=section_dto.is_active,
            section_type=section_type.id,
            page_id=section_dto.page_id,
            contents=section_dto.contents
            )

        db.session.add(section)
        db.session.commit()
        db.session.flush()

        return section.id

    def convert_to_dto(self, section:Section):
        section_type_id = section.section_type

        # Get the content type by ID.
        section_type = SectionType.query.get(section_type_id)
        section_type_dto = None
        if section_type != None:
            section_type_dto = SectionTypeDTO(
                id=section_type.id,
                name=section_type.name,
                description=section_type.description
            )
        
        dto = SectionDTO(
            id=section.id,
            name=section.name,
            is_active=section.is_active,
            section_type=section_type_dto,
            page_id=section.page_id,
            contents=section.contents
        )
        return dto

    def get_section_by_id(self, id: int):
        # Read the content by ID.
        section = Section.query.get(id)
        dto = None
        if section != None:
            dto = self.convert_to_dto(section=section)
        return dto

    def get_sections_by_page(self, page_id:int, full_details:bool=False):
        sections = Section.query.filter_by(page_id=page_id).all()
        section_dtos = []
        if sections != None:
            content_service = ContentService()
            for section in sections:
                section_dto = self.convert_to_dto(section=section)
                if full_details:
                    content_dtos = content_service.get_content_by_section_id(section_dto.id)
                    section_dto.contents = content_dtos
                section_dtos.append(section_dto)
        return section_dtos

    def update_section(self, section_dto:SectionDTO):
        section_type = section_dto.section_type
        if section_type == None:
            raise Exception("Section type is required for section.")

        #content = db.session.get(Content, content_dto.id, with_for_update=True)
        section = Section.query.get(section_dto.id)

        if section != None:
            section.name = section_dto.name
            section.is_active = section_dto.is_active
            section.section_type = section_type.id
            #section.page_id=section_dto.page_id
            #section.contents=section_dto.contents
        
            db.session.commit()
        else:
            raise Exception(f"Section with id {section_dto.id} not found.")

    def section_validation(self, section:dict):
        result = {}
        status = "error"
        error_msg = ""
        success_msg = ""
        data = None
        if section == None or not section:
            error_msg = "Something went wrong"
        else:
            section_name = section.get("section_name", None)
            section_type = section.get("section_type", None)
                
            section_name_err = None
            section_type_err = None
            
            has_error = False
            if section_name == None or not section_name:
                section_name_err = "Please enter valid section name."
                has_error = True
            if section_type == -1 or not section_type:
                section_type_err = "Please select section type."
                has_error = True
            if not has_error:
                status = "success"
                success_msg = "Section created successfully."
            
            data = {}
            if section_name_err != None:
                data["section_name"] = section_name_err
            if section_type_err != None:
                data["section_type"] = section_type_err
        result['status'] = status
        if error_msg != None and error_msg:
            result['error_msg'] = error_msg
        if success_msg != None and success_msg:
            result['success_msg'] = success_msg
        if data != None:
            result['data'] = data
        return result

    def delete_section_by_id(self, section_id:int):
        section = Section.query.filter_by(id=section_id).first() 
        db.session.delete(section)
        db.session.commit()

