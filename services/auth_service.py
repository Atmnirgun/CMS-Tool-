from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from services.user_service import UserService
class AuthService:

    @staticmethod
    def is_logged_in():
        if session.get("username") == None:
            return redirect(url_for("pages.login_page"))
        return True

    @staticmethod
    def auth_user(user_creds):
        user_service = UserService()
        
        result = {}
        status = "error"
        error_msg = None
        data = None
        if user_creds == None or not user_creds:
            error_msg = "Something went wrong, credentials not found."
        else:
            username = user_creds["username"]
            password = user_creds["password"]
            
            username_err = None
            password_err = None
            
            has_error = False
            if username == None or not username:
                username_err = "Please enter valid user name."
                has_error = True
            if password == None or not password:
                password_err = "Please enter valid password."
                has_error = True
            if not has_error:
                userData = user_service.get_user_by_username(username=username)
                if userData != None:
                    password_db = userData.password
                    if password_db == None:
                        error_msg = "User not found!"
                    else:
                        if password_db != password:
                            error_msg = "Please enter valid credentials, user password does not match."
                        else:
                            status = "success"
                            session['username'] = username
                else:
                    error_msg = "username not found"
                            
            data = {}
            if username_err != None:
                data["username"] = username_err
            if password_err != None:
                data["password"] = password_err
        result['status'] = status
        if error_msg != None and error_msg:
            result['error_msg'] = error_msg
        if data != None:
            result['data'] = data
        return result
