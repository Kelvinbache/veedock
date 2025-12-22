// button
const sendButton = document.getElementById("send_up")

// form
const form_login = document.getElementById("form_up")

// user
const username = document.getElementById("username_up")

// email
const email = document.getElementById("email_up")


// password
const passwor = document.getElementById("passwor_up")
const passwor_config = document.getElementById("password_config_up")

async function send(e){

    e.preventDefault();

    if (passwor.value === passwor_config.value){

     const data = {
       username:username.value,
       email:email.value,
       passwor:passwor.value
      }


    await fetch("http://127.0.0.1:8090/token/login_up",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify(data)
    })
    
    .then(response => {
        console.log(response)
   
    }).catch(errr => {
        return errr
    })
   
} else {
    return "password not valid"
}
    
}

sendButton.addEventListener("submit", send);