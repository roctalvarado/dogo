document.getElementById("btn-register").addEventListener("click", register);

function register(){
    password = document.getElementById("user-password").value;
    confirmPassword = document.getElementById("user-confirm-password").value;

    if(password != confirmPassword) {
        alert("Las contraseñas no coinciden.")
        return;

        // sweetalert
    }

    const data = {
        name: document.getElementById("user-name").value,
        email: document.getElementById("user-email").value,
        password: password
    }

    //endpoint
    fetch('api/users', {
        method:"POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    }).then(response => response.json())
    .then(result => {
        if(result.success) {
            alert("Usuario se guardó correctamente")
        } else {
            alert(result.message)
        }
    })
    .catch(error => {
        console.error(error);
    })

}