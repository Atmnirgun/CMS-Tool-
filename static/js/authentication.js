function reset_validation_styles() {

   let err_generic = document.getElementById('feedback')
   let err_user = document.getElementById('user_feedback')
   let err_password = document.getElementById('password_feedback')
   if(err_generic){
      err_generic.textContent =""
   }
   if(err_password){
      err_password.textContent =""
   }
   if(err_user){
      err_user.textContent =""
   }
   
   let user= document.getElementById("username").classList.remove('is-invalid');
   let pwd = document.getElementById("password").classList.remove('is-invalid');
}

function signin() {
   
   // Reset the validation styles.
   reset_validation_styles();

   let user= document.getElementById("username").value;
   let pwd = document.getElementById("password").value;
   
   var url = "api/authenticate"
   var data={username:user, password:pwd}
   params = {
      method : 'POST',
      headers : {
         'Content-Type' : 'application/json',
         'Accept' : 'application/json'
      },
      body : JSON.stringify(data)
   }

   fetch(url, params).then((response) => {
      return response.json();
   }).then((result) => {      
      if(result.status === "success"){
            var login_form = document.getElementById("login_form")
            if(login_form){
               login_form.submit()
            }
      } else {
            data = result.data
            error_msg = result.error_msg;
            if(error_msg){
               let err = document.getElementById('feedback')
               err.textContent = result.error_msg
            }
            if("username" in data)
            {
               //error = data["username"]
               var id = document.getElementById('username')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('user_feedback')
               err.textContent = result.data.username
            }
            if ("password" in data)
            {
               //error = data["password"]
               var id = document.getElementById('password')
               let cList = id.classList
               cList.add('is-invalid')
               let err = document.getElementById('password_feedback')
               err.textContent = result.data.password
            }
      }
   })
}
 