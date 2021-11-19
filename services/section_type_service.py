from db.entities import SectionType
from db.orm import orm
from models.section_dto import SectionTypeDTO

class SectionTypeService:

    def get_by_id(self, id:int):
        result = SectionType.query.get(id)
        dto = None
        if result != None:
            dto = SectionTypeDTO(
                    id=result.id,
                    name=result.name,
                    description=result.description
                )
        return dto

    def get_all(self):
        res = SectionType.query.all()
        dtos = []
        if res != None:
            for sec_type in res:
                dto = SectionTypeDTO(
                    id=sec_type.id,
                    name=sec_type.name,
                    description=sec_type.description
                )
                dtos.append(dto)
        return dtos