#EN ESTE ARCHIVO SE DEFINEN LOS ESQUEMAS DE LA BASE DE DATOS DE LA APLICACIÓN.#

from flask_sqlalchemy import SQLAlchemy
import bcrypt
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

BD = SQLAlchemy()

###DEFINICIÓN DE ESQUEMAS DE LA BASE DE DATOS###

#ESQUEMA DE USUARIOS#
class Usuario(BD.Model):

    #NOMBRE DE LA TABLA#
    __tablename__ = "usuarios"

    #DECLARACIÓN DE ATRIBUTOS#
    id = BD.Column(BD.Integer, primary_key = True)
    nombre = BD.Column(BD.String(60))
    apellido = BD.Column(BD.String(60))
    email = BD.Column(BD.Text(), unique = True)
    clave = BD.Column(BD.Text())
    #RELACIÓN CON OTRA TABLA: REPOSITORIO#
    repositorios = BD.relationship('Repositorio', back_populates = 'usuario', cascade = 'all, delete')

    """CONSTRUCTOR"""

    def __init__(self, nombre, apellido, email, clave):

        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.clave = self.Encriptar(clave)


    #ENCRIPTAR CONTRASEÑA#
    def Encriptar(self, clave):
        return generate_password_hash(clave)
    #VERIFICACIÓN DE CONTRASEÑA INGRESADA POR EL USUARIO#


    def ValidarClave(self, clave):
        return check_password_hash(self.clave, clave)

#MODELADO DE REPOSITORIOS#
class Repositorio(BD.Model):

    #NOMBRE DE LA TABLA#
    __tablename__ = "repositorios"

    #ATRIBUTOS DE LA TABLA#
    idRepo = BD.Column(BD.Integer, primary_key = True)
    idUsuario = BD.Column(BD.Integer, BD.ForeignKey('usuarios.id', ondelete='CASCADE', onupdate='CASCADE'))
    usuario = BD.relationship('Usuario', back_populates = 'repositorios')
    nombre_repo = BD.Column(BD.Text())
    #RELACIÓN CON OTRA TABLA: IMAGENES#
    imagenes = BD.relationship('Imagen', back_populates = 'repo', cascade = 'all, delete')

    """CONSTRUCTOR"""

    def __init__(self, idUsuario, nombre_repo):

        self.idUsuario = idUsuario
        self.nombre_repo = nombre_repo

#MODELO DE IMÁGENES#

class Imagen(BD.Model):

    #NOMBRE DE LA TABLA#
    __tablename__ = 'imagenes'
    #ATRIBUTOS DE LA TABLA#
    idImagen = BD.Column(BD.Integer, primary_key = True)
    idRepo = BD.Column(BD.Integer, BD.ForeignKey('repositorios.idRepo', ondelete='CASCADE', onupdate='CASCADE'))
    repo = BD.relationship('Repositorio', back_populates = 'imagenes')
    nombre_img = BD.Column(BD.String(50))
    autor = BD.Column(BD.String(60))
    tags = BD.Column(BD.String(100))
    url = BD.Column(BD.Text())

    """CONSTRUCTOR"""

    def __init__(self, idRepo, nombre_img, autor, url, tags):
        self.idRepo = idRepo
        self.nombre_img = nombre_img
        self.autor = autor
        self.tags = tags
        self.url = url
        


