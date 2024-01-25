# RUTAS PARA LOGUIARSE Y REGISTRARSE.

# IMPORTARMOS 
from flask import request,Blueprint
from .. import db
from main.models import UsuarioModels
from flask_jwt_extended import create_access_token #PARA CREAR TOKEN
from main.auth.decorators import user_identity_lookup
from main.mail.functions import send_mail


#Esta línea está configurando un Blueprint que es un prefijo llamado 'auth' que contendrá rutas relacionadas
#con la autenticación, y todas esas rutas estarán bajo la URL '/auth'.

#sirve para estructurar y organizar el codigo de aplicaciones web

auth=Blueprint('auth', __name__,url_prefix='/auth')


@auth.route('/login',methods=['POST'])


def login():

    usuario= db.session.query(UsuarioModels).filter(UsuarioModels.email==request.get_json().get('email')).first_or_404()
    
    if usuario.validate_password(request.get_json().get('password')):

#una vez validada la contraseña
        
        access_token= create_access_token(identity=usuario)

#de vuelve el token al usuario
        data={
            'id': str(usuario.id),
            'email': usuario.email,
            'access_token': access_token,
            'role': str(usuario.role)
        }

        return data,200
    
    else:
        return 'Incorrect password',401



@auth.route('/register',methods=['POST'])
def register():
    usuario= UsuarioModels.from_json(request.get_json())
    exits=db.session.query(UsuarioModels).filter(UsuarioModels.email==usuario.email).scalar() is not None

    if exits == True :
        return 'Duplicated email',409
    else:
        try:
            db.session.add(usuario)
            db.session.commit()
            send_mail([usuario.email],'bienvenido','register', usuario = usuario)
        except Exception as error:
            db.session.rollback()
            return str(error),409
        return usuario.to_json(),201