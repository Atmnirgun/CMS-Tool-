function reset_validation_styles() {

    let cname_err = document.getElementById('cname_feedback')
    let ctype_err = document.getElementById('ctype_feedback')
    let contents_err = document.getElementById('content_feedback')
    if(cname_err){
       cname_err.textContent =""
    }
    if(ctype_err){
       ctype_err.textContent =""
    }
    if(contents_err){
       contents_err.textContent =""
    }
    
    let cname= document.getElementById("contentname").classList.remove('is-invalid');
    let ctype = document.getElementById("content_type").classList.remove('is-invalid');
    let contents = document.getElementById("contents").classList.remove('is-invalid');
 }

function handleContentTypeChange() {
    let con_type = document.getElementById('content_type');
    let id = con_type.value;

    let textbox = document.getElementById('contents');
    let richbox = document.getElementById('standalone-container');

    if (id === '1') {
        textbox.classList.add('d-none');
        richbox.classList.remove('d-none');
    } else {
        richbox.classList.add('d-none');
        textbox.classList.remove('d-none');
    }
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
            let form = document.getElementById("content_form")
            form.classList.add('d-none')
            let return_button = document.getElementById("return")
            return_button.classList.remove("d-none")
            document.getElementById('sectionId').value = result.data.id
            
        }else{
            data = result.data
            error_msg = result.error_msg;

            if(error_msg){
               let err = document.getElementById('error_feedback')
               err.textContent = result.error_msg
            }
            if("content_name" in data)
            {
               var id = document.getElementById('contentname')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('cname_feedback')
               err.textContent = result.data.content_name
            }
            if ("content_type" in data)
            {
               var id = document.getElementById('content_type')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('ctype_feedback')
               err.textContent = result.data.content_type
            }
            if ("contents" in data)
            {
               var id = document.getElementById('contents')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('content_feedback')
               err.textContent = result.data.contents
            }
        }
    })
}

function create_content() {
    reset_validation_styles();
    let content_name = document.getElementById("contentname").value;
    let contents = document.getElementById("contents").value;
    let content_type = document.getElementById("content_type");
    let content_type_id = parseInt(content_type.options[content_type.selectedIndex].value);
    let section_id = parseInt(document.getElementById("sectionId").value);    
    let activate_check = false
    if(document.querySelector('.form-check-input').checked){
        activate_check = Boolean(document.getElementById("activate").value);
    }

    if (content_type_id === 1) {
        contents = document.getElementsByClassName('ql-editor')[0].innerHTML;
    }
    var url = "/api/content"
    var data = {content_name:content_name, 
        content_type:content_type_id, 
        contents:contents, 
        activate_check:activate_check,
        section_id:section_id    
    }

    submit_req(url, data, 'POST')
}

function update_content() {
    reset_validation_styles();
    let content_name = document.getElementById("contentname").value;
    let content_id = parseInt(document.getElementById("content_id").value);
    let contents = document.getElementById("contents").value;
    let content_type = document.getElementById("content_type");
    let section_id = parseInt(document.getElementById("sectionId").value);   
    let content_type_id = parseInt(content_type.options[content_type.selectedIndex].value);
    let activate_check = false
    if(document.querySelector('.form-check-input').checked){
        activate_check = Boolean(document.getElementById("activate").value);
    }
    if (content_type_id === 1) {
        contents = document.getElementsByClassName('ql-editor')[0].innerHTML;
    }
    
    var url = "/api/content/"+ content_id
    var data={content_id:content_id,
        content_name:content_name,
        content_type:content_type_id,
        contents:contents,
        activate_check:activate_check,
        section_id:section_id
    }

    submit_req(url, data, 'PUT')
}

function delete_content(){
    let id = document.getElementById('id').textContent;
    console.log(id);
    var url = "/api/content/delete/"+id
    var data={content_id:id}
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
    document.getElementById("content_form").reset();  
}