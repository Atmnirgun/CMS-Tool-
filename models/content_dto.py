import json

class ContentTypeDTO:

    def __init__(self, id:int, name:str, description:str):
        self.id = id
        self.name = name
        self.description = description

 
class ContentDTO:
    
    def __init__(self, id:int, name:str, content_type:ContentTypeDTO, section_id:int, 
        is_active:bool, data:str, section=None):
        self.id = id
        self.name = name
        self.content_type = content_type
        self.section_id = section_id
        self.section = section
        self.data = data
        self.is_active = is_active

