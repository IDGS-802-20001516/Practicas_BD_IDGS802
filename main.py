from flask import Flask, request,render_template,Response
import forms
from flask_wtf.csrf import CSRFProtect
from flask import g 
from config import DevelopmentConfig
from flask import flash
from models import db
from models import Maestros
from models import Alumnos
app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route("/maestros",methods=["GET","POST"])
def maestros():
    maestro_form=forms.UserForm2(request.form)
    if request.method=='POST' and maestro_form.validate():
        maestro=Maestros(nombre=maestro_form.nombre.data,
                    apaterno=maestro_form.apaterno.data,
                    edad=maestro_form.edad.data,
                    email=maestro_form.email.data,
                    profesion=maestro_form.profesion.data,
                    direccion=maestro_form.direccion.data,
                    numt=maestro_form.numt.data)
        db.session.add(maestro)
        db.session.commit()
    return render_template("maestros.html", form=maestro_form)


@app.route("/ABC_CompletoMaestros",methods=["GET","POST"])
def ABCompleto():
    maestro=""
    
  
    maestro=Maestros.query.all()
    return render_template("ABC_CompletoMaestros.html",maestros=maestro)

@app.route("/alumnos",methods=["GET","POST"])
def alumnos():
    alum_form=forms.UserForm1(request.form)
    if request.method=='POST' and alum_form.validate():
        alum=Alumnos(nombre=alum_form.nombre.data,
                    apaterno=alum_form.apaterno.data,
                    email=alum_form.email.data)
        db.session.add(alum)
        db.session.commit()
    return render_template("alumnos.html", form=alum_form)


@app.route("/ABC_CompletoAlumnos",methods=["GET","POST"])
def ABCompletoA():
    alumno=""
    
  
    alumno=Alumnos.query.all()
    return render_template("ABC_CompletoAlumnos.html",alumnos=alumno)



if __name__=="__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    app.run()