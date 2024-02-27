from wtforms import Form
from wtforms import StringField, TextAreaField, SelectField, RadioField, EmailField, IntegerField
from wtforms import validators

class UserForm(Form):
    nombre = StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido'), 
        validators.length(min=4, max=10, message="Ingresa nombre valido")
    ])
    email = EmailField("Correo", [
        validators.Email(message="Ingresa el correo valido")
    ])
    apaterno = StringField("apaterno")
    materias = SelectField(choices=[("Espanol", "Esp",), ("Mat", "matematicas"), ('Ingles', 'ING')])
    edad = IntegerField('edad', [
        validators.number_range(min=1, max=28, message="Valor no valido")
    ])

    radios = RadioField('Curso', choices=[('1', '1'), ('2','2'), ('3','3')])

class UserForm1(Form):
    id=IntegerField('id')
    nombre=StringField("nombre",[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=4,max=10,message='ingresa nombre valido')])
    
    apaterno=StringField('apaterno')
    email=EmailField('correo',[
        validators.Email(message='Ingrese un correo valido'
                         )])

class UserForm2(Form):
    id=IntegerField('id')
    nombre=StringField("NOMBRE",[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=4,max=20,message='ingresa nombre valido')])
    
    apaterno=StringField("APELLIDO PATERNO",[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=4,max=35,message='ingresa apellido valido')])
    edad = IntegerField('EDAD', [
        validators.number_range(min=1, max=99, message="Valor no valido")
    ])
    email=EmailField("CORREO",[
        validators.Email(message='Ingrese un correo valido'
                         )])
    profesion=StringField("PROFESION",[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=4,max=30,message='ingresa profesion valida')])
    direccion=StringField("DIRECCION",[validators.DataRequired(message='el campo es requerido'),
                                 validators.length(min=4,max=30,message='ingresa direccion valida')])
    numt = StringField("NUMERO TELEFONICO", [
        validators.Length(min=10, max=10, message="Debe tener exactamente 10 dígitos"),
        validators.Regexp('^[0-9]+$', message="Debe contener solo dígitos")
    ])

    