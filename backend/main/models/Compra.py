from .. import db
import datetime as dt

class Compra( db.Model):

    id=db.Column(db.Integer,primary_key=True)
    fecha_compra=db.Column(db.DateTime,default=dt.datetime.now(),nullable=False)
    usuarioID= db.Column(db.Integer, db.ForeignKey('usuario.id'),nullable=False)
    usuario=db.relationship('Usuario',back_populates='compras',uselist=False,single_parent=True)
    productoscompras=db.relationship('ProductoCompra',back_populates='compra',cascade='all, delete-orphan')

    def __repr__(self):
        return f'Compra:{self.usuarioID}'
    
    def to_json(self):
        compra_json={
            'id':self.id,
            'fecha_compra': str(self.fecha_compra),
            'usuario': self.usuario.to_json(),
        }

        return compra_json
    
    @staticmethod
    def from_json(compra_json):
        id=compra_json.get('id')
        fecha_compra=compra_json.get('fecha_compra')
        usuarioID=compra_json.get('usuarioID')

        return Compra(
            id=id,
            fecha_compra=fecha_compra,
            usuarioID=usuarioID

        )