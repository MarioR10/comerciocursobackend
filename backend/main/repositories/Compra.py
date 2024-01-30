# se encarga de interactuar con la db

from .. import db
from main.models import CompraModels

class CompraRepository:
    __modelo= CompraModels

    @property
    def modelo(self):
        return self.__modelo
    
    def find_one(self,id):
        object= db.session.query(self.modelo).get(id)
        return object
    
    def find_all(self,id):
        object= db.session.query(self.modelo).all()
        return object
    
    def create(self,object):
        db.session.add(object)
        db.session.commit()
        return object
    
    def update(self,object):
        return self.create(object)
    
    def delete(self,id):
        object=self.find_one(id)
        db.session.delete(object)
        db.session.commit()
        return object
    
    

