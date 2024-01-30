from flask_restful import Resource
from main.maps.Compra import CompraSchema
from main.services import CompraService
from flask import request

compra_schema=CompraSchema()
compra_service=CompraService()

class CompraControllers(Resource):

    def get(self,id):
        compra= compra_service.obtener_compra_con_descuento(id)
        return compra_schema.dump(compra,many= False)
    

class ComprasControllers(Resource):

    def post(self):
        compra= compra_schema.load(request.get_json())
        return compra_schema.dump(compra_service.agregar_compra(compra), many=False) 