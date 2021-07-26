from wtforms import form
from werkzeug.utils import secure_filename
import Forms
from config import *
from flask import Flask, redirect, request, render_template, session, jsonify, flash
from modelos import BD
from modelos import Usuario, Repositorio, Imagen
import os

#MIDDLEWARE PARA LA CREACIÓN DE DIRECTORIO PARA LAS IMÁGENES EN CASO DE NO EXISTIR#
def GenerarDirectorio():
    cwd = os.getcwd()
    ruta = os.path.join(cwd, 'public', 'assets/imagenes')

    if(os.path.isdir(ruta)):
        print("El directorio ya existe.")
    else:
        print('Creando directorio...')
        os.mkdir(ruta)


#INSTANCIA DE LA APLICACIÓN DE FLASK#
app = Flask(__name__, static_folder = 'public/', static_url_path='/', template_folder='public/views')
app.config.from_object(DevelopmentConfig)

#SI OCURRE UN ERROR DE 404, SE ENVÍA UN MENSAJE AL USUARIO#
@app.errorhandler(404)
def not_found(error):
    return "Error 404. Recurso no encontrado."

#PÁGINA PRINCIPAL DE LA APLICACIÓN#
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

#VALIDACIÓN DE RUTAS(VERIFICACIÓN DE SESIÓN)#

@app.before_request
def ValidarSesion():
    if 'idU' not in session and request.endpoint not in ['index','Registro', 'InicioSesion', 'static']:
        print('No está en sesión.', request.endpoint);
        mensaje = "No está autenticado. Por favor, inicie sesión pulsando el botón para iniciar sesión"
        flash(mensaje)
        return redirect('/')

@app.after_request
def SesionValidada(respuesta):
    return respuesta



#FIN VALIDACIÓN DE RUTAS#

#REGISTRO Y AUTENTICACIÓN DE USUARIOS EN LA APLICACIÓN#
@app.route('/Registro',methods = ['GET', 'POST'])
def Registro():
    RegistroUF = Forms.FormularioRegistro(request.form)
    if request.method == 'POST' and RegistroUF.validate():
        Cuenta = Usuario.query.filter_by(email = RegistroUF.email.data).first()
        print(request.method, Cuenta)
        if Cuenta is None:

            #SE CREA EL NUEVO USUARIO SI TODOS LOS DATOS SON CORRECTOS.
            NuevoU = Usuario(nombre = RegistroUF.nombre.data,
            apellido = RegistroUF.apellido.data,
            email = RegistroUF.email.data,
            clave = RegistroUF.clave.data)

            BD.session.add(NuevoU)
            BD.session.commit()


            print(RegistroUF.email.data)
            mensaje = "¡Su cuenta ha sido creada con éxito! Por favor, inicie sesión"
            flash(mensaje)
            return redirect('/')

        else:
            mensaje = "El email ingresado ya está en uso. Por favor, ingrese uno diferente."
            flash(mensaje)
            return redirect('/Registro')


    return render_template('Registro.html', form = RegistroUF)


@app.route('/IniciarSesion', methods = ['GET', 'POST'])
def InicioSesion():
    FormularioInicioSesion = Forms.FormularioInicioS(request.form)

    if request.method == 'POST' and FormularioInicioSesion.validate():
        EmailU = FormularioInicioSesion.email.data
        ClaveU = FormularioInicioSesion.clave.data
        print("La clave que ingresó el usuario es: ", ClaveU)

        #SE VALIDAN LAS CREDENCIALES#

        Usuario_Sesion = Usuario.query.filter_by( email = EmailU).first()
        if Usuario_Sesion is not None and Usuario_Sesion.ValidarClave(ClaveU):
            session['idU'] = Usuario_Sesion.id
            session['email'] = EmailU
            session['nombre'] =Usuario_Sesion.nombre
            return redirect('/Inicio', )
        else:
            mensaje = "Email o contraseña incorrectas, por favor, verifique sus datos."
            flash(mensaje)
            return redirect('/IniciarSesion')
            
    return render_template('InicioSesion.html', form = FormularioInicioSesion)

@app.route('/Salir', methods = ['GET'])
def CerrarSesion():
    if 'email' in session:
        session.pop('email');
        session.pop('nombre');
        session.pop('idU');
        return redirect('/');

#FIN DE REGISTRO Y AUTENTICACIÓN DE USUARIOS#


#USUARIO Y CREACIÓN DE REPOSITORIOS-IMÁGENES

@app.route('/Usuarios/VerPerfil')
def VerPerfil():
    return render_template('PerfilUsuario.html')

#VISUALIZAR LOS DATOS DEL USUARIO#
@app.route('/Usuarios/MostrarDatosU', methods = ['GET'])
def MostrarDatos():
    id_Usuario = session.get('idU')
    DatosUsuario = Usuario.query.filter_by(id = id_Usuario).first()
    ReposUsuario = Repositorio.query.filter_by(idUsuario = session.get('idU')).all()
    Repos_Usuario = []

    #SE UBICAN LOS REPOSITORIOS QUE SON PROPIEDAD DEL USUARIO#
    for repo in ReposUsuario:
        datos_repo = {
            "idRepo" : repo.idRepo,
            "idUsuario" : repo.idUsuario,
            "nombre_repo" : repo.nombre_repo
        }
        Repos_Usuario.append(datos_repo)
    
    return jsonify({"estado": 200, "NombreU": DatosUsuario.nombre, "ApellidoU": DatosUsuario.apellido, "EmailU": DatosUsuario.email, "Repos": Repos_Usuario}), 200

#CREAR UN NUEVO REPOSITORIO#
@app.route('/CrearRepositorio', methods = ['GET', 'POST'])
def DespachoFormularioCol():
    ColFormulario = Forms.FormularioRepositorios(request.form)

    if request.method == 'POST' and ColFormulario.validate():
        print('El nombre del repo es: ', ColFormulario.nombre.data)
        NuevoRepo = Repositorio(session.get('idU'), ColFormulario.nombre.data)
        BD.session.add(NuevoRepo)
        BD.session.commit()

        return redirect('/Usuarios/VerPerfil')

    return render_template('CrearRepositorio.html', form = ColFormulario)

#VISUALIZAR UN REPOSITORIO ESPECÍFICO#
@app.route('/VerRepositorio/<idR>', methods=['GET'])
def VerRepositorio(idR):
    print('el id del repositorio es: ', idR)

    DatosRepo = Repositorio.query.filter_by(idRepo = idR).first()
    ImagenesRepo = Imagen.query.filter_by(idRepo = idR).all()
    print('Las imagenes de este repositorio son: ', ImagenesRepo)

    imagenes_repo = []

    for i in ImagenesRepo:
        datosImagen = {
            "idImagen" : i.idImagen,
            "idRepo" : i.idRepo,
            "nombre_img" : i.nombre_img,
            "autor" : i.autor,
            "tags" : i.tags,
            "url" : i.url 
        }
        imagenes_repo.append(datosImagen) 
    
    print(imagenes_repo)
    Resultado = {
        "nombre_repo" : DatosRepo.nombre_repo,
        "idRepo" : DatosRepo.idRepo,
        "idUsuario" : DatosRepo.idUsuario,
        "imagenes" : imagenes_repo
        }
    
    print(Resultado)
    return render_template('VerRepo.html', datos = Resultado, emailUsuario = session.get('email'), nombreUsuario = session.get('nombre'))

#ELIMINAR UN REPOSITORIO#
@app.route('/BorrarRepositorio/<id>', methods = ['DELETE'])
def BorrarRepositorio(id):
    print(id)
    Repo = Repositorio.query.filter_by(idRepo = id).first()
    BD.session.delete(Repo)
    BD.session.commit()
    return "Ok"

#AGREGAR IMÁGENES A UN REPOSITORIO#
@app.route('/AgregarImagen/<idRepo>', methods = ['GET', 'POST'])
def AgregarImagen(idRepo):
    print(idRepo)
    
    
    if request.method == 'POST':
        print('Creando imagen...')
        #SE OBTIENE LA RUTA DEL ARCHIVO PARA GUARDARLA EN LA BD, Y SE ALMACENA EL ARCHIVO EN LA CARPETA#
        archivo = request.files['file']
        archivo.save(os.getcwd() + "/public/assets/imagenes/" + secure_filename(archivo.filename))
        url = "/assets"+"/imagenes/"+archivo.filename
        Nueva_img = Imagen(idRepo, request.form['titulo'], session.get('nombre'), url, request.form['tags'])
        #SE AGREGA LA IMAGEN CREADA A LA COLECCIÓN CORRESPONDIENTE#
        BD.session.add(Nueva_img)
        BD.session.commit()
        return redirect('/VerRepositorio/'+idRepo)

    return render_template('NuevaImagen.html', idRepo = idRepo)

#ELIMINAR UNA IMAGEN#
#SE REALIZA CON EL MÉTODO HTTP - GET PARA AHORRO DE ESCRITURA DE RUTAS#
@app.route('/BorrarImagen/<id>', methods = ['GET'])
def BorrarImagen(id):
    print(id)
    BImagen = Imagen.query.filter_by(idImagen = id).first()
    BD.session.delete(BImagen)
    BD.session.commit()
    mensaje = "La imagen ha sido borrada con éxito. Revise el repositorio pertinente para agregar nuevas imágenes."
    flash(mensaje)
    return redirect('/Usuarios/VerPerfil')

#BÚSQUEDA DE PUBLICACIONES POR MEDIO DE LAS ETIQUETAS#
@app.route('/ResultadosBusqueda/<Datos>', methods = ['GET'])
def ResultadosBusqueda(Datos):
    print(Datos)

    Resultados = Imagen.query.filter_by(tags = Datos).all()
    RespuestaBusqueda = []
    for imagen in Resultados:
        datos_imagen = {
            "idImagen" : imagen.idImagen,
            "idRepo" : imagen.idRepo,
            "nombre_img" : imagen.nombre_img,
            "autor" : imagen.autor,
            "tags" : imagen.tags,
            "url" : imagen.url
        }
        RespuestaBusqueda.append(datos_imagen)
    
    return render_template('Busqueda.html', imagen = RespuestaBusqueda, emailUsuario = session.get('email'), nombreUsuario = session.get('nombre') )

#EDICIÓN DE USUARIOS#
@app.route('/Usuarios/Editar', methods = ['GET'])
def Editar():
    FormularioEdicion = Forms.FormularioRegistro(request.form)

    return render_template('EditarUsuario.html', form = FormularioEdicion)

@app.route('/Usuarios/EditarU', methods = ['PUT'])
def EditarU():
    FormularioEdicion = Forms.FormularioRegistro(request.form)
    print(FormularioEdicion.email.data)
    usuario = Usuario.query.filter_by(id = session.get('idU')).first()
    usuario.nombre = FormularioEdicion.nombre.data
    usuario.apellido = FormularioEdicion.apellido.data
    usuario.email = FormularioEdicion.email.data
    usuario.clave = FormularioEdicion.clave.data
    session['idU'] = usuario.id
    session['email'] = usuario.email
    session['nombre'] = usuario.nombre

    BD.session.commit()


    return "Ok"

#ELIMINAR USUARIO#
@app.route('/Usuarios/Borrar', methods = ['DELETE'])
def Borrar():
    BorrarUsuario = Usuario.query.filter_by(email = session.get('email')).first()
    BD.session.delete(BorrarUsuario)
    BD.session.commit()
    mensaje = "Su cuenta ha sido eliminada con éxito."
    flash(mensaje)
    return "Su cuenta ha sido eliminada con éxito."


#DESPACHO DEL INICIO DE LA APLICACIÓN UNA VEZ AUTENTICADO#

@app.route('/Inicio', methods = ['GET'])
def DespachoInicio():
    UsuarioIdentificado = session.get('email')
    a = session.get('nombre')
    #BUSCAR TODAS LAS PUBLICACIONES#
    publicaciones = Imagen.query.all()
    Posts = []
    for i in publicaciones:
        datosImagen = {
            "idImagen" : i.idImagen,
            "idRepo" : i.idRepo,
            "nombre_img" : i.nombre_img,
            "autor" : i.autor,
            "tags" : i.tags,
            "url" : i.url 
        }
        Posts.append(datosImagen)


    return render_template('InicioDupic.html', emailUsuario = UsuarioIdentificado, nombreUsuario = a, imagenes = Posts)


###########################################################

BD.init_app(app)


# Iniciar servidor (ejecutar)
if __name__ == '__main__':

    with app.app_context():
        BD.create_all()
    
    GenerarDirectorio()
    app.run()