function reset_validation_styles() {

    let sname_err = document.getElementById('sname_feedback')
    let stype_err = document.getElementById('stype_feedback')
    
    if(sname_err){
       sname_err.textContent =""
    }
    if(stype_err){
       stype_err.textContent =""
    }
    
    let cname= document.getElementById("sectionname").classList.remove('is-invalid');
    let ctype = document.getElementById("section_type").classList.remove('is-invalid');
 }

function submit_req(url, data, http_method){
    req_params = {
        method : http_method,
        headers : {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json'
        },
        body : JSON.stringify(data)
    }

    fetch(url, req_params).then((response)=>{
        return response.json();
    }).then((result)=>{
        
        if(result.status === "success"){
            let message_block = document.getElementById('success_feedback')
            //message.textContent = result.success_msg
            message_block.classList.remove("d-none")
            document.getElementById("success_msg").textContent = result.success_msg
            let form = document.getElementById("section_form")
            form.classList.add('d-none')
            let div = document.getElementById("sec")
            div.classList.remove("d-none")
            let section_info = result.data
            if (section_info) {
                document.getElementById('sec_name').textContent = section_info.section_name
                document.getElementById('sec_type').textContent = section_info.section_type.name
                document.getElementById('is_active').textContent = section_info.activate_check
                let addButton = document.getElementById('btn-add-content')
                addButton.setAttribute("href","/content?sectionId="+section_info.id)
                //console.log(addButton.href)
            } else {
                // TODO - Add error message.
                document.getElementById('section-data').textContent = "Something went wrong!"
            }
        } else {
            data = result.data
            error_msg = result.error_msg;

            if(error_msg){
               let err = document.getElementById('error_feedback')
               err.textContent = result.error_msg
            }
            if("section_name" in data)
            {
               var id = document.getElementById('sectionname')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('sname_feedback')
               err.textContent = result.data.section_name
            }
            if ("section_type" in data)
            {
               var id = document.getElementById('section_type')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('stype_feedback')
               err.textContent = result.data.section_type
            }
        }
    })
}

function submit_update_req(url, data, http_method){
    req_params = {
        method : http_method,
        headers : {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json'
        },
        body : JSON.stringify(data)
    }

    fetch(url, req_params).then((response)=>{
        return response.json();
    }).then((result)=>{
        
        if(result.status === "success"){
            let message_block = document.getElementById('success_feedback')
            //message.textContent = result.success_msg
            message_block.classList.remove("d-none")
            document.getElementById("success_msg").textContent = result.success_msg
            let form = document.getElementById("section_form")
            form.classList.add('d-none')
            let return_button = document.getElementById("return")
            return_button.classList.remove("d-none")
            let section_info = result.data
            if (section_info) {
                document.getElementById('sec_name').textContent = section_info.section_name
                document.getElementById('sec_type').textContent = section_info.section_type.name
                document.getElementById('is_active').textContent = section_info.activate_check
                let addButton = document.getElementById('btn-add-content')
                addButton.setAttribute("href","/content?sectionId="+section_info.id)
                //console.log(addButton.href)
            } else {
                // TODO - Add error message.
                document.getElementById('section-data').textContent = "Something went wrong!"
            }
        } else {
            data = result.data
            error_msg = result.error_msg;

            if(error_msg){
               let err = document.getElementById('error_feedback')
               err.textContent = result.error_msg
            }
            if("section_name" in data)
            {
               var id = document.getElementById('sectionname')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('sname_feedback')
               err.textContent = result.data.section_name
            }
            if ("section_type" in data)
            {
               var id = document.getElementById('section_type')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('stype_feedback')
               err.textContent = result.data.section_type
            }
        }
    })
}

function create_section() {
    reset_validation_styles();
    let section_name = document.getElementById("sectionname").value;
    let section_type = document.getElementById("section_type");
    let section_type_id = parseInt(section_type.options[section_type.selectedIndex].value);    
    let page_id = parseInt(document.getElementById("page_id").value);
    let activate_check = false
    if(document.querySelector('.form-check-input').checked){
        activate_check = Boolean(document.getElementById("activate").value);
    }

    var url = "/api/section"
    var data = {section_name:section_name, 
        section_type:section_type_id,  
        activate_check:activate_check,
        page_id:page_id
    }

    submit_req(url, data, 'POST')
}

function update_section() {
    reset_validation_styles();
    let section_name = document.getElementById("sectionname").value;
    let section_id = parseInt(document.getElementById("section_id").value);
    let page_id = parseInt(document.getElementById("page_id").value);
    let section_type = document.getElementById("section_type");
    let section_type_id = parseInt(section_type.options[section_type.selectedIndex].value);
    let activate_check = false
    if(document.querySelector('.form-check-input').checked){
        activate_check = Boolean(document.getElementById("activate").value);
    }
    
    var url = "/api/section/"+ section_id
    var data={section_id:section_id,
        section_name:section_name,
        section_type:section_type_id,
        activate_check:activate_check,
        //page_id:page_id
    }

    submit_update_req(url, data, 'PUT')
}

function delete_section(){
    let id = document.getElementById('id').textContent;
    console.log(id);
    var url = "/api/section/delete/"+id
    var data={section_id:id}
    submit_delete_req(url, data, 'DELETE')
}

function submit_delete_req(url, data, http_method){
    req_params = {
        method : http_method,
        headers : {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json'
        },
        body : JSON.stringify(data)
    }

    fetch(url, req_params).then((response)=>{
        return response.json();
    }).then((result)=>{
        if("success" in result){
            let id = document.getElementById("delete_div")
            id.classList.add("d-none")
            let message_block = document.getElementById('success_feedback')
            message_block.classList.remove("d-none")
            document.getElementById("success_msg").textContent = result.success
            let return_button = document.getElementById("return")
            return_button.classList.remove("d-none")
        }
        if ("error" in result){
            let id = document.getElementById("delete_div")
            id.classList.add("d-none")
            let message_block = document.getElementById('error_feedback')
            message_block.classList.remove("d-none")
            document.getElementById("error_msg").textContent = result.error
        }
    })
}

function resetdata(){  
    document.getElementById("section_form").reset();  
}