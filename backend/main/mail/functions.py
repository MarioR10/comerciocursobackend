from .. import mailsender,db
from flask import current_app,render_template,Blueprint
from flask_mail import Message
from smtplib import SMTPException
from main.models import UsuarioModels,ProductoModels
from main.auth.decorators import role_required


# Definir la función para enviar correos electrónicos
def send_mail(to,subject,template,**kwargs):

# Crear una instancia de la clase Message con el asunto, el remitente y quien lo recibe configurados
    
    msg=Message(subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=to)

    try:

        # Configurar el cuerpo del mensaje utilizando un archivo de plantilla (template.txt)

        msg.body=render_template(f'{template}.txt',**kwargs)

        # Enviar el correo electrónico utilizando la instancia de mailsender
        mailsender.send(msg)

# Manejar cualquier excepción SMTPException que pueda ocurrir durante el envío
    except SMTPException as error:
        return 'Mail deliver failed'
    
# Retornar True si el correo electrónico se envía correctamente
    return True


mail=Blueprint('mail',__name__,url_prefix='/mail')


@mail.route('/newsletter', methods=['POST'])
@role_required(roles=['admin'])
def newsletter():

    usuarios= db.session.query(UsuarioModels).filter(UsuarioModels.role=='cliente').all()
    productos= db.session.query(ProductoModels).all()

    try: 
        for usuario in usuarios:

            send_mail([usuario.email], 'Productos en venta', 'newsletter',usuario=usuario,productos= [producto.nombre for producto in productos])

    except SMTPException as error:
        return 'Mail deliver failed'
    return 'mail sent',200