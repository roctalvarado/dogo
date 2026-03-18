document.getElementById("btn-signin").addEventListener("click, login");

function login(){
    email: document.getElementById("user-email").value;
    password: document.getElementById("user-password").value;

    if(email == "") {
        alert("Debe ingresar su correo electrónico")
        // TODO: Completar con sweet alert
    }

    if(password == "") {
        alert("Debe ingresar su contraseña")
        // TODO: Completar con sweet alert
    }

    const data = {
        email: email,
        password: password
    }

    //endpoint
    fetch('api/login', {
        method:"POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(data)
    }). then(response => response.json())
    .then(result =>  {
        if(result.success){
            window.location.href = "/welcome"
        } else {
            alert("Sus datos de acceso no son correctos")
            // TODO : Completar con sweet alert
        }
    })
    .catch(error => {
        console.error(error);
    })
}