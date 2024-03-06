from flask_sqlalchemy import SQLAlchemy
import datetime


db=SQLAlchemy()

class Alumnos(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    apaterno=db.Column(db.String(50))
    email=db.Column(db.String(50))
    create_date=db.Column(db.DateTime,default=datetime.datetime.now)

class Maestros(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    apaterno=db.Column(db.String(50))
    edad=db.Column(db.Integer)
    email=db.Column(db.String(50))
    profesion=db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    numt=db.Column(db.String(10))
    create_date=db.Column(db.DateTime,default=datetime.datetime.now)

class Pizzas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    tamanio = db.Column(db.String(20))
    ingredientes = db.Column(db.String(200))
    num = db.Column(db.Integer)
    subtotal = db.Column(db.Float)
    create_date=db.Column(db.DateTime,default=datetime.datetime.now)