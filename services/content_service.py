from db.entities import Content, ContentType
from db.orm import db

from models.content_dto import ContentDTO, ContentTypeDTO

class ContentService():

    def create_content(self, content_dto:ContentDTO):
        content_type = content_dto.content_type
        if content_type == None:
            raise Exception("Content type is required for content.")

        section_id = None
        if content_dto.section != None:
            section_id = content_dto.section.id

        content = Content(id=content_dto.id, 
            name=content_dto.name, 
            data=content_dto.data, 
            is_active=content_dto.is_active,
            content_type=content_type.id,
            section_id=section_id)

        db.session.add(content)
        db.session.commit()
        db.session.flush()

    def update_content(self, content_dto:ContentDTO):
        content_type = content_dto.content_type
        if content_type == None:
            raise Exception("Content type is required for content.")

        
        #content = db.session.get(Content, content_dto.id, with_for_update=True)
        content = Content.query.get(content_dto.id)

        if content != None:
            content.name = content_dto.name
            content.data = content_dto.data
            content.is_active = content_dto.is_active
            content.content_type = content_type.id
            content.section_id = content_dto.section_id

            db.session.commit()
        else:
            raise Exception(f"Content with id {content_dto.id} not found.")

    def get_content_all(self):
        contents = Content.query.all()
        res = []
        for content in contents:
            dto = ContentDTO(id=content.id, name=content.name, data=content.data,
            content_type=None, section_id=1)
            res.append(dto)

        return res

    def get_content_by_id(self, id: int):
        # Read the content by ID.
        content = Content.query.get(id)
        dto = None
        if content != None:
            content_type_id = content.content_type

            # Get the content type by ID.
            content_type = ContentType.query.get(content_type_id)
            content_type_dto = None
            if content_type != None:
                content_type_dto = ContentTypeDTO(
                    id=content_type.id,
                    name=content_type.name,
                    description=content_type.description
                )
           
            dto = ContentDTO(
                id=content.id,
                name=content.name,
                data=content.data,
                is_active=content.is_active,
                content_type=content_type_dto,
                section_id=content.section_id
            )
        return dto

    def get_content_by_section_id(self,sectionId:int):
        contents = Content.query.filter_by(section_id=sectionId).all()
        dtos = []
        if contents != None:
            for content in contents:
                content_type_id = content.content_type

                # Get the content type by ID.
                content_type = ContentType.query.get(content_type_id)
                content_type_dto = None
                if content_type != None:
                    content_type_dto = ContentTypeDTO(
                        id=content_type.id,
                        name=content_type.name,
                        description=content_type.description
                    )
            
                dto = ContentDTO(
                    id=content.id,
                    name=content.name,
                    data=content.data,
                    is_active=content.is_active,
                    content_type=content_type_dto,
                    section_id=content.section_id
                )
                dtos.append(dto)
        return dtos
        
    def delete_content_by_id(self, content_id:int):
        content = Content.query.filter_by(id=content_id).first() 
        db.session.delete(content)
        db.session.commit()

    