document.getElementById("btn-signin").addEventListener("click", login);

function login(){
    const email = document.getElementById("user-email").value;
    const password = document.getElementById("user-password").value;

    if(email == "") {
        Swal.fire({
            icon: 'warning',
            title: 'Campo requerido',
            text: 'Debe ingresar su correo electrónico.'
        });
        return;
    }

    if(password == "") {
        Swal.fire({
            icon: 'warning',
            title: 'Campo requerido',
            text: 'Debe ingresar su contraseña.'
        });
        return;
    }

    const data = {
        email: email,
        password: password
    }

    //endpoint
    fetch('/api/login', {
        method:"POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(data)
    }). then(response => response.json())
    .then(result =>  {
        if(result.success){
            window.location.href = "/welcome"
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error de acceso',
                text: result.message
            });
        }
    })
    .catch(error => {
        console.error(error);
    })
}