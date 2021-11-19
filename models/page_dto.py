class PageDTO:

    def __init__(self, id:int, name:str, is_active:bool, 
        user_id:int, sections:list):
        self.id = id
        self.name = name
        self.is_active = is_active
        self.user_id = user_id
        self.sections = sections