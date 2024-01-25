from flask_restful import Resource
from flask import request,jsonify
from .. import db
from main.models import ProductoCompraModels



class ProductosCompras(Resource):
    def get(self):

        page=1
        per_page= 5
        max_per_page=8

        productoscompras=db.session.query(ProductoCompraModels)

        if request.get_json():
            filters=request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page=int(value)
                
                elif key== 'per_page':
                    per_page=int(value)    
        productoscompras=productoscompras.paginate(page=page,per_page=per_page,error_out=True, count=True, max_per_page=max_per_page)
        
        return jsonify(

            {
                'productoscompras': [productocompra.to_json() for productocompra in productoscompras.items],
                'total': productoscompras.total,
                'pages': productoscompras.page,
                'page': page
            }
            
        )
        
    
    def post(self):
        productocompra= ProductoCompraModels.from_json(request.get_json())
        db.session.add(productocompra)
        db.session.commit()
        return productocompra.to_json(),201

        
class ProductoCompra(Resource):
    def get(self,id):
        productocompra=db.session.query(ProductoCompraModels).get_or_404(id)
        try: 
            return productocompra.to_json()
        except:
            return 'error al obtener los datos',404
    
    def delete(self,id):
        productocompra = db.session.query(ProductoCompraModels).get_or_404(id)
        try:
            db.session.delete(productocompra)
            db.session.commit()
            return 'ha sido eliminado',204
        
        except:
            return 'error en eliminar',404
        
    def put(self,id):
        productocompra=db.session.query(ProductoCompraModels).get_or_404(id)
        data= request.get_json().items()
        for key, value in data:

            setattr(productocompra,key,value)

        try: 
            db.session.add(productocompra)
            db.session.commit()
            return productocompra.to_json(),201
        
        except:
            return 'error al modificar el dato',404
