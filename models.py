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

