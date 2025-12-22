const sendButton = document.getElementById("send")
const form_login = document.getElementById("form")
const username = document.getElementById("username")
const passwor = document.getElementById("passwor")

async function send(e){

    e.preventDefault();
    
    const data = {
       username:username.value,
       passwor:passwor.value
    }

    await fetch("http://127.0.0.1:8090/token/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:data
    })
    
    .then(response => {
        console.log(response)
    }).catch(errr => {
        return errr
    })
   
    

}

sendButton.addEventListener("submit", send) 