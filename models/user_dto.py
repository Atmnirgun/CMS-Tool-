class UserDTO:

    def __init__(self, id:int, user_name:str, first_name:str, 
        last_name:str, password:str, email_id:str, is_active:bool):
        
        self.id = id
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email_id = email_id
        self.is_active = is_active