from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import UsuarioModels

class Usuario(Resource):
    def get(self,id):
        usuario=db.session.query(UsuarioModels).get_or_404(id)
        return usuario.to_json()
    
    def delete(self,id):
        usuario=db.session.query(UsuarioModels).get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    
    def put(self,id):

        usuario= db.session.quety(UsuarioModels).get_or_404(id)
        data= request.get_json().items()

        for key,value in data:
            setattr(usuario,key,value)
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(),201

class Usuarios(Resource):
    def get(self):
        page=1
        per_page= 5
        max_per_page=8

        ususarios= db.session.query(UsuarioModels)

        if request.get_json():
            filters=request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page=int(value)
                
                elif key== 'per_page':
                    per_page=int(value)    
        ususarios=ususarios.paginate(page=page,per_page=per_page,error_out=True, count=True, max_per_page=max_per_page)
        
        return jsonify(

            {
                'usuarios': [ususario.to_json() for ususario in ususarios.items],
                'total': ususarios.total,
                'pages': ususarios.page,
                'page': page
            }
            
        )
