function reset_validation_styles() {

    let pname_err = document.getElementById('pname_feedback')
    if(pname_err){
       pname_err.textContent =""
    }
    let pname= document.getElementById("pagename").classList.remove('is-invalid');
 }

function create_page() {
    reset_validation_styles();
    let page_name = document.getElementById("pagename").value;
    let user_id = parseInt(document.getElementById("userId").value);
    let activate_check = false
    if(document.querySelector('.form-check-input').checked){
        activate_check = Boolean(document.getElementById("activate").value);
    }
    var url = "/api/page"
    var data={
        page_name:page_name,
        activate_check:activate_check,
        user_id:user_id
    }

    submit_req(url, data, 'POST')
}

function update_page() {
    reset_validation_styles();
    let page_name = document.getElementById("pagename").value;
    let page_id = parseInt(document.getElementById("page_id").value);
    let activate_check = false
    if(document.querySelector('.form-check-input').checked){
        activate_check = Boolean(document.getElementById("activate").value);
    }
    var url = "/api/page/"+page_id
    var data={
        page_name:page_name,
        activate_check:activate_check
    }

    submit_req(url, data, 'PUT')
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
            message_block.classList.remove("d-none")
            document.getElementById("success_msg").textContent = result.success_msg
            let form = document.getElementById("page_form")
            form.classList.add('d-none')
            let return_button = document.getElementById("return")
            return_button.classList.remove("d-none")
            if(result.data){
                let backButton = document.getElementById('btn-back-to-home')
                backButton.setAttribute("href", "/page/" + result.data)
                document.getElementById("btn-back").textContent = "Return to page"
            }

        }else{
            data = result.data
            if("page_name" in data)
            {
               var id = document.getElementById('pagename')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('pname_feedback')
               err.textContent = result.data.page_name
            }
        }
    })
}

function delete_page(){
    let id = document.getElementById('id').textContent;
    console.log(id);
    var url = "/api/page/delete/"+id
    var data={page_id:id}
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
