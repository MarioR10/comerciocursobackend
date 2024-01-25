from flask_restful import Resource
from flask import jsonify,request
from .. import db
from main.models import UsuarioModels
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity

class Cliente(Resource):


    @role_required(roles=['admin','cliente'])
    def get(self,id):
        cliente=db.session.query(UsuarioModels).get_or_404(id)
        current_user= get_jwt_identity()

        if cliente.role == 'cliente':

            if current_user['usuarioID']== cliente.id or current_user['role']== 'admin':
                return cliente.to_json()
            else:
                return 'Unauthorized',401
                
        else:
            return 'El ID no corresponde a un cliente', 404


    @role_required(roles=['cliente'])
    def delete(self, id):

        cliente=db.session.query(UsuarioModels).get_or_404(id)
        current_user =get_jwt_identity()

        if cliente.role == 'cliente' and current_user['usuarioID']== cliente.id:
            try:
                db.session.delete(cliente)
                db.committ()
                return 'eliminado con exito',204
            except:
                return 'hubo un error al eliminar al cliente',404
        else:
            return 'Unauthorized'
        

        
    @role_required(roles=['cliente'])
    def put(self,id):
        cliente=db.session.query(UsuarioModels).get_or_404(id)
        current_user=get_jwt_identity()

        if cliente.role == 'cliente' and current_user['usuarioID']== cliente.id:

            data= request.get_json().items()

            for key,value in data:

                setattr(cliente,key,value)
            
            try: 
                db.session.add(cliente)
                db.session.commit()
                return cliente.to_json(),201
            
            except:
                return 'Hubo una falla en el proceso de modificar cliente',404
            
        else:
            return 'Unauthorized'
        
        
class Clientes(Resource):

    @role_required(roles=['admin'])
    def get(self):

        page=1
        per_page= 5
        max_per_page=8

        clientes=db.session.query(UsuarioModels).filter(UsuarioModels.role=='cliente')

        if request.get_json():
            filters=request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page=int(value)
                
                elif key== 'per_page':
                    per_page=int(value)    
        clientes=clientes.paginate(page=page,per_page=per_page,error_out=True, count=True, max_per_page=max_per_page)
        
        return jsonify(

            {
                'clientes': [cliente.to_json() for cliente in clientes.items],
                'total': clientes.total,
                'pages': clientes.page,
                'page': page
            }
            
        )

    def post(self):
        cliente=UsuarioModels.from_json(request.get_json())
        cliente.role= 'cliente'
        db.session.add(cliente)
        db.session.commit()
        return cliente.to_json(),201   



