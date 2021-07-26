boton = document.getElementById('Eliminar');

//FUNCIÓN PARA ELIMINAR EL USUARIO
const Borrar = (e) =>{
    fetch('/Usuarios/Borrar', {method: 'DELETE'}).then(res =>{return res.text()}).then(res =>{window.location.href = '/'})
}

boton.onclick = Borrar;



