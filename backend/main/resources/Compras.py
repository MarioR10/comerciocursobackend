from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import CompraModels
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity

class Compra(Resource):

    @role_required(roles=['admin','cliente'])
    def get(self,id):
        compra= db.session.query(CompraModels).get_or_404(id)
        current_user= get_jwt_identity()
        if current_user['usuarioID']==compra.usuarioID or current_user['role']== 'admin':
            try:
                return compra.to_json()
            
            except:
                return 'eror en obtener compra',404
        else: 
            return 'Unauthorized',401

    @role_required(roles=['admin','cliente'])  
    def put(self,id):
        compra=db.session.query(CompraModels).get_or_404(id)
        current_user= get_jwt_identity()
        if current_user['usuarioID']==compra.usuarioID or current_user['role']== 'admin':
            data= request.get_json().items()
            for key,value in data:

                setattr(compra,key,value)
                try:
                    db.session.add(compra)
                    db.session.commit()
                    return compra.to_json(),201
                except:
                    return 'error al editar la compra',404
                
        else:
            return 'Unauthorized',401


class Compras(Resource):

    @role_required(roles=['admin'])
    def get(self):
        page=1
        per_page= 5
        max_per_page=8

        compras=db.session.query(CompraModels)

        if request.get_json():
            filters=request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page=int(value)
                
                elif key== 'per_page':
                    per_page=int(value)    
        compras=compras.paginate(page=page,per_page=per_page,error_out=True, count=True, max_per_page=max_per_page)
        return jsonify(
            {
                'compras': [compra.to_json() for compra in compras.items],
                'total': compras.total,
                'pages': compras.page,
                'page': page
            }
        )
    @role_required(roles=['admin', 'cliente'])
    def post(self):
        
        compra= CompraModels.from_json(request.get_json())
        print(compra, flush=True)
        db.session.add(compra)
        db.session.commit()
        return compra.to_json(),201