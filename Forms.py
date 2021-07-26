#EN ESTE ARCHIVO SE DEFINIRÁN LOS FORMULARIOS FLASK PARA LAS DISTINTAS TOMAS DE DATOS DE LA MISMA#
from wtforms import Form, StringField, TextField, PasswordField, FileField
from wtforms.fields.html5 import EmailField
from wtforms import validators

#FORMULARIO PARA REGISTRO/EDICIÓN DE USUARIO#
class FormularioRegistro(Form):
    nombre = StringField('Nombre: ', [
        validators.length(min=4, max=60, message="Por favor, ingrese un nombre de entre 4 a 60 caracteres.")
    ])
    apellido = StringField('Apellido: ',[
        validators.length(min=4, max=60, message="Por favor, ingrese un apellido de entre 4 a 60 caracteres.")
    ])
    email = EmailField('Email: ',[
        validators.Required(message = 'Este campo es requerido y no puede quedar en blanco.')
    ])
    clave = PasswordField('Contraseña: ', [
        validators.length(min = 4, message = 'La contraseña debe contener como mínimo 4 caracteres.')
    ])

#FORMULARIO PARA INICIO DE SESIÓN DEL USUARIO#
class FormularioInicioS(Form):
    email = EmailField('Email: ',[
        validators.Required(message = 'Este campo es requerido y no puede quedar en blanco.')
    ])
    clave = PasswordField('Contraseña: ', [validators.Required('Este campo es requerido y no puede quedar en blanco.')])  
    
#FORMULARIO PARA CREACIÓN DE COLECCIONES#
class FormularioRepositorios(Form):
    nombre = StringField('Nombre del repositorio: ', [
        validators.Required(message='Este campo es requerido.')
    ])

#FORMULARIO PARA CREACIÓN DE IMÁGENES
class FormularioImagenes(Form):
    nombre_img = StringField('Nombre de la imagen: ', [
        validators.Required(message = "Este campo no puede quedar vacío."),
    ])
    tags = StringField('Etiqueta(s): ',[
        validators.Required(),
        validators.length(max = 100, message = "Este campo no puede superar los 100 caracteres.")
    ])
    