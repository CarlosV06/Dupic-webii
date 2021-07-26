//EN ESTE ARCHIVO SE DEFINE LA FUNCIÓN PARA MOSTRAR LA INFORMACIÓN DEL USUARIO 

//FUNCIÓN PARA TRAER LOS DATOS DEL USUARIO Y MOSTRARLOS AL CLIENTE

const MostrarDatos= (e) =>{
    fetch('/Usuarios/MostrarDatosU', {method: 'GET'}).then(res =>{
        return res.json();
    }).then(res =>{
        console.log(res.estado+res.EmailU);
        let Padre = document.getElementById('Info');
        let Padre2 = document.getElementById('ReposU');
        let nombre = document.createElement('p');
        let apellido = document.createElement('p');
        let email = document.createElement('p');
        nombre.innerText = "Nombre: "+res.NombreU;
        apellido.innerText = "Apellido: "+res.ApellidoU;
        email.innerText = "Correo electrónico: "+res.EmailU;
        Padre.appendChild(nombre);
        Padre.appendChild(apellido);
        Padre.appendChild(email);
        for (i = 0; i < res.Repos.length; i++){
            let ContenedorRepo = document.createElement('div');
            let Nombre_Repo = document.createElement('p');
            let VerR = document.createElement('input');
            let BorrarR = document.createElement('input');
            let EditarR = document.createElement('input');
            BorrarR.value = "Borrar";
            BorrarR.type = "button";
            BorrarR.id = res.Repos[i].idRepo;
            BorrarR.style = 'border-radius: 10px; background-color: red; color: white';

            //FUNCIONALIDAD PARA EL BOTÓN DE BORRAR REPOSITORIO
            BorrarR.onclick = (e) =>{
                console.log(e.target.id);
                fetch('/BorrarRepositorio/'+e.target.id, {method: 'DELETE'}).then(res =>{return res.text()}).then(res =>{
                    if(res == 'Ok'){
                        alert(res);
                        window.location.href = '/Usuarios/VerPerfil';
                    }
                })


            }


            VerR.type = 'button';
            VerR.style = 'border-radius: 10px; background-color: dodgerblue; color: white';
            VerR.value = "Ver";
            VerR.id = res.Repos[i].idRepo;
            VerR.onclick = (e) =>{
                fetch('/VerRepositorio/'+e.target.id, {method: 'GET'}).then(res =>{
                    return res.status;
                }).then(res =>{
                    window.location.href = "/VerRepositorio/"+e.target.id;
                })
            }
            //-SE DEFINE LA FUNCIONALIDAD DEL BOTÓN VER, 
            //EL CUAL MOSTRARÁ LAS IMÁGENES DE DICHO REPOSITORIO, Y PERMITIRÁ AGREGAR IMÁGENES AL MISMO-
            ContenedorRepo.id = res.Repos[i].idRepo;
            ContenedorRepo.style = "background: -webkit-linear-gradient(0deg, rgba(34,193,195,1) 0%, rgba(253,187,45,1) 100%);; border-radius: 0.5rem; border-color: black; width: 20%; text-align: center; float: left; margin-top: 25px; margin-left: 40px;"
            Nombre_Repo.innerText = res.Repos[i].nombre_repo;
            Nombre_Repo.style = "color: white;"
            ContenedorRepo.appendChild(Nombre_Repo);
            ContenedorRepo.appendChild(VerR);
            ContenedorRepo.appendChild(BorrarR);
            //ContenedorRepo.appendChild(EditarR);
            Padre2.appendChild(ContenedorRepo);
        }
    })
}



window.onload = MostrarDatos;