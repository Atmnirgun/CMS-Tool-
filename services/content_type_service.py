from db.entities import ContentType
from db.orm import orm
from models.content_dto import ContentTypeDTO

class ContentTypeService:

    def get_by_id(self, id:int):
        result = ContentType.query.get(id)
        dto = None
        if result != None:
            dto = ContentTypeDTO(
                    id=result.id,
                    name=result.name,
                    description=result.description
                )
        return dto

    def get_all(self):
        res = ContentType.query.all()
        dtos = []
        if res != None:
            for con_type in res:
                dto = ContentTypeDTO(
                    id=con_type.id,
                    name=con_type.name,
                    description=con_type.description
                )
                dtos.append(dto)
        return dtos