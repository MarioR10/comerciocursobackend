
# IMPORTACIONES 

import os 
from flask import Flask
from dotenv import load_dotenv

#importar modulo para crear la APIREST
from flask_restful import Api

#importo modulo para conectar con una BD sql

from flask_sqlalchemy import SQLAlchemy

#importar modulo para trabajar con JWT

from flask_jwt_extended import JWTManager

# importar modulo para trabajar con envio de email
from flask_mail import Mail

# INSTANCIAS 
api=Api()
db=SQLAlchemy()
jwt=JWTManager()
mailsender= Mail()


# CREACION DE SERVIDOR

def createApp():

    app= Flask(__name__)  

#cargar variables de entorno
    load_dotenv()

#configuracion base de datos, EN EL SISTEMA OPERATIVO
    
    PATH= os.getenv("DATABASE_PATH")
    DB_NAME= os.getenv("DATABASE_NAME")
    if not os.path.exists(f'{PATH}{DB_NAME}'):
        os.chdir(f'{PATH}')
        file=os.open(f'{DB_NAME}',os.O_CREAT).close()
        
##TERMINA AQUI
        
    #CONECTARSE A LA BASE DE DATOS  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{PATH}{DB_NAME}'
    db.init_app(app)


    import main.resources as resources
    import main.controllers as controllers
    api.add_resource(resources.ClientesResource, '/clientes')
    api.add_resource(resources.ClienteResource, '/cliente/<id>')
    api.add_resource(resources.UsuariosResource, '/Usuarios')
    api.add_resource(resources.UsuarioResource, '/Usuario/<id>')
    api.add_resource(resources.ComprasResource, '/compras')
    api.add_resource(resources.CompraResource, '/compra/<id>')
    api.add_resource(resources.ProductosResource,'/productos')
    api.add_resource(resources.ProductoResource,'/producto/<id>')
    api.add_resource(resources.ProductosComprasResource,'/produtos-compras')
    api.add_resource(resources.ProductoCompraResource,'/produto-compra/<id>')
    api.add_resource(controllers.CompraControllers, '/compra-controller/<id>')
    api.add_resource(controllers.ComprasControllers, '/compras-controller')
    
    
    
    api.init_app(app)

    #CONFIGURAR JWT

    # Configuración de la clave secreta para firmar tokens JWT
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    # Configuración del tiempo de expiración de los tokens de acceso JWT
    app.config['JWT_ACCESS_TOKEN_EXPIRES']= int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    # Inicialización
    jwt.init_app(app)

#blueprint
    from main.auth import routes
    app.register_blueprint(auth.routes.auth)

    from main.mail import functions
    app.register_blueprint(mail.functions.mail)

    # configurar mail

    app.config['MAIL_HOSTNAME']=os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER']=os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT']=os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS']=os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME']=os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD']=os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER']=os.getenv('FLASKY_MAIL_SENDER')

    mailsender.init_app(app)


    return app