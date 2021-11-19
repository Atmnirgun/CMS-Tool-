from services.section_service import SectionService

def content_validation(content:dict):
        result = {}
        status = "error"
        error_msg = ""
        success_msg = ""
        data = None
        section_dto = None
        if content == None or not content:
            error_msg = "Something went wrong"
        else:
            content_name = content.get("content_name", None)
            content_type = content.get("content_type", None)
            contents = content.get("contents", None)  
            section_id = content.get("section_id", None)
                
            content_name_err = None
            content_type_err = None
            contents_err = None
            section_id_err = None
            has_error = False
            if content_name == None or not content_name:
                content_name_err = "Please enter valid content name."
                has_error = True
            if content_type == -1 or not content_type:
                content_type_err = "Please select content type."
                has_error = True
            if contents == None or not contents:
                contents_err = "Please enter valid contents."
                has_error = True
            if section_id == None or not section_id:
                section_id_err = "Please enter valid section."
                has_error = True
            else:
                section_service = SectionService()
                section_dto = section_service.get_section_by_id(section_id)
                if section_dto == None:
                    section_id_err = f"Section for given section id {section_id} not found."
                    has_error = True

            if not has_error:
                status = "success"
                success_msg = "content created successfully."
            
            data = {}
            if content_name_err != None:
                data["content_name"] = content_name_err
            if content_type_err != None:
                data["content_type"] = content_type_err
            if contents_err != None:
                data["contents"] = contents_err
            if section_id_err != None:
                data["section_id"] = section_id_err
        result['status'] = status
        if error_msg != None and error_msg:
            result['error_msg'] = error_msg
        if success_msg != None and success_msg:
            result['success_msg'] = success_msg
        if data != None:
            result['data'] = data
        
        return (result, section_dto)

