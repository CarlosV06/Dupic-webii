#ESTE ARCHIVO DEFINIRÁ UNA SERIE DE CONFIGURACIONES PARA LA APLICACIÓN.#

import os

class Config(object):
    SECRET_KEY = "alzate pato que mañana te cocino."
    SQLALCHEMY_DATABASE_URI = "postgresql://sqpcxjlgbndbhk:cc1d28c62a28ab64a32305a64ed8d7d242abaf41f40cd2199ee3fc15be623dd7@ec2-52-0-67-144.compute-1.amazonaws.com:5432/dbg0h7k8517kh2"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


"""SE DEFINE LA CONFIGURACIÓN DE DESARROLLO"""
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

"""SE DEFINE LA CONFIGURACIÓN DE PRODUCCIÓN"""
class ProductionConfig(Config):
    DEBUG = False
