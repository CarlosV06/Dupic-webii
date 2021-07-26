
let boton = document.getElementById('Enviar');


const Enviar = (e) =>{
    console.log(e.target.id);
    let FormularioUsuario = document.getElementById('EditarFormulario');
    let Datos = new FormData(FormularioUsuario);
    for (const value of Datos.values()) {
        console.log(value)
    }
    fetch('/Usuarios/EditarU',{method: 'PUT', body: Datos}).then(res =>{return res.text()}).then(res =>{if(res == 'Ok'){
        window.location.href = '/Usuarios/VerPerfil';
    }})
    


}

boton.onclick = Enviar;
