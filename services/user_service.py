from db.orm import db
from models.user_dto import UserDTO
from db.entities import User

class UserService():

    def get_user_by_username(self,username:str):
        user = User.query.filter_by(user_name=username).first()
        return user

    def create_user(self,user_dto:UserDTO):
        user = User(id=user_dto.id,
            user_name=user_dto.user_name,
            first_name=user_dto.first_name, 
            last_name=user_dto.last_name,
            email_id=user_dto.email_id,
            password=user_dto.password,
            is_active=user_dto.is_active)
        db.session.add(user)
        db.session.commit()

    def user_data_validation(self,user_data:dict):
        result = {}
        status = "error"
        error_msg = ""
        success_msg = ""
        data = None
        if user_data == None or not user_data:
            error_msg = "Something went wrong"
        else:
            user_name = user_data.get("user_name", None)
            first_name = user_data.get("first_name", None)
            last_name = user_data.get("last_name", None)
            email = user_data.get("email",None)
            password = user_data.get("password",None)  
                
            user_name_err = None
            first_name_err = None
            last_name_err = None
            email_err = None
            password_err = None
            has_error = False
            if user_name == None or not user_name:
                user_name_err = "Please enter valid user name."
                has_error = True
            if first_name == None or not first_name:
                first_name_err = "Please enter valid first name."
                has_error = True
            if last_name == None or not last_name:
                last_name_err = "Please enter valid last name."
                has_error = True
            if email == None or not email:
                email_err = "Please enter valid email."
                has_error = True
            if password == None or not password:
                password_err = "Please enter valid password."
                has_error = True
            if not has_error:
                status = "success"
                success_msg = "Registered successfully."
            
            data = {}
            if user_name_err != None:
                data["user_name"] = user_name_err
            if first_name_err != None:
                data["first_name"] = first_name_err
            if last_name_err != None:
                data["last_name"] = last_name_err
            if email_err != None:
                data["email"] = email_err
            if password_err != None:
                data["password"] = password_err
        result['status'] = status
        if error_msg != None and error_msg:
            result['error_msg'] = error_msg
        if success_msg != None and success_msg:
            result['success_msg'] = success_msg
        if data != None:
            result['data'] = data

        if result["status"] == "success":
            user = User.query.filter_by(user_name=user_name).first()
            if user == None:
                result["status"] == "success"
            else:
                result["status"] = "error"
                result["user_name_duplicate_error"] = "username already exist please try another"
        #check status is success
        #get user from database by username
        #if user is none that means username is new send suucess response
        #else update the data object with username duplication error  data["user_name"] = "username already exist please try another"
        print(result)
        return result






