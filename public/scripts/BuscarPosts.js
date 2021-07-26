//EN ESTE ARCHIVO SE DEFINE LA BÚSQUEDA DE POSTS MEDIANTE LOS TAGS INGRESADOS POR EL USUARIO
//FUNCIÓN PARA REALIZAR ENVÍO Y REDIRECCIÓN A LA RUTA PERTINENTE PARA MOSTRAR LOS RESULTADOS DE LA BÚSQUEDA
const BotonBuscar = document.getElementById("Busqueda");


const BuscarC = (e) =>{
    
    e.preventDefault();
    const Datos = document.getElementById("Dato").value;
    fetch('/ResultadosBusqueda/'+Datos, {method: 'GET'}).then(res =>{return res.status}).then(res =>{window.location.href = '/ResultadosBusqueda/'+Datos })
}

BotonBuscar.onclick = BuscarC;