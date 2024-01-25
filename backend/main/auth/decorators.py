from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt


#
#

def role_required(roles):
    def decorator(funcion):
        def wrapper(*args,**kwargs):

            # verificar que el JWT es correcto
            verify_jwt_in_request()
            #obtenermos los claims (peticiones), que estan dentro del JWT
            claims=get_jwt()
            #VERIFICO EL ROL
            if claims['sub']['role'] in roles:
                return funcion(*args,**kwargs)
            else:
                return 'Roll not allowed',403
            
        return wrapper
    return decorator



# decoradores que ya trae el jwt, pero los redefinimos

@jwt.user_identity_loader
def user_identity_lookup(usuario):
    # NO SE GUARDAN DATOS SENSIBLES YA QUE NO ESTA INCRIPTADO, INFORMACION QUE LLEVA EL TOKEN
    return{
        'usuarioID': usuario.id,
        'role': usuario.role
    }


@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):

    #Devuelve informacion adicional CON EL TOKEN
    
    claims={

        'id': usuario.id,
        'role': usuario.role,
        'email':usuario.email #NO DEBERIAMOS DE GUARDARLO, SE HACE POR EJEMPLO PERO NO SE DEBERIA
    }
