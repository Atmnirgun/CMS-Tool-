class SectionTypeDTO:

    def __init__(self, id:int, name:str, description:str):
        self.id = id
        self.name = name
        self.description = description

class SectionDTO:

    def __init__(self, id:int, name:str, section_type:SectionTypeDTO, 
        page_id:int, is_active:bool, contents:list):

        self.id = id
        self.name = name
        self.section_type = section_type
        self.page_id = page_id
        self.is_active = is_active
        self.contents = contents