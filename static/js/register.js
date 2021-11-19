function reset_validation_styles() {
    let err_username = document.getElementById('uname_feedback')
    let err_firstname = document.getElementById('fname_feedback')
    let err_lastname = document.getElementById('lname_feedback')
    let err_email = document.getElementById('email_feedback')
    let err_password = document.getElementById('password_feedback')
    if(err_username){
        err_username.textContent =""
    }
    if(err_firstname){
        err_firstname.textContent =""
    }
    if(err_lastname){
        err_lastname.textContent =""
    }
    if(err_email){
        err_email.textContent =""
    }
    if(err_password){
        err_password.textContent =""
    }
    let usern= document.getElementById("username").classList.remove('is-invalid');
    let fname = document.getElementById("firstname").classList.remove('is-invalid');
    let lname = document.getElementById("lastname").classList.remove('is-invalid');
    let email = document.getElementById("email").classList.remove('is-invalid');
    let pwd = document.getElementById("password").classList.remove('is-invalid');
 }
function create_user(){
    reset_validation_styles();
    let user_name = document.getElementById("username").value;
    let first_name = document.getElementById("firstname").value;
    let last_name = document.getElementById("lastname").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let activate_check = false
    if(document.querySelector('.form-check-input').checked){
        activate_check = Boolean(document.getElementById("active").value);
    }
    //console.log(user_name)
    var url = "/api/register"
    var data = {user_name:user_name,
        first_name:first_name, 
        last_name:last_name,
        email:email,
        password:password, 
        activate_check:activate_check}

    submit_req(url, data, 'POST')
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
            let form = document.getElementById("registration_form")
            form.classList.add('d-none')
        }else{
            data = result.data
            error_msg = result.error_msg;

            if(error_msg){
               let err = document.getElementById('error_feedback')
               err.textContent = result.error_msg
            }
            if("user_name_duplicate_error" in result)
            {
                var id = document.getElementById('username')
                let cList = id.classList
                cList.add('is-invalid')
                let err = document.getElementById('uname_feedback')
                err.textContent = result.user_name_duplicate_error 
            }
            if("user_name" in data)
            {
               var id = document.getElementById('username')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('uname_feedback')
               err.textContent = result.data.user_name
            }
            if ("first_name" in data)
            {
               var id = document.getElementById('firstname')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('fname_feedback')
               err.textContent = result.data.first_name
            }
            if ("last_name" in data)
            {
               var id = document.getElementById('lastname')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('lname_feedback')
               err.textContent = result.data.last_name
            }
            if ("email" in data)
            {
               var id = document.getElementById('email')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('email_feedback')
               err.textContent = result.data.email
            }
            if ("password" in data)
            {
               var id = document.getElementById('password')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('password_feedback')
               err.textContent = result.data.password
            }
        }
    })
}

function resetdata(){  
    document.getElementById("registration_form").reset();  
}