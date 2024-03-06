from flask import Flask, request,render_template,Response,redirect,url_for
import forms
from flask_wtf.csrf import CSRFProtect
from flask import g 
from config import DevelopmentConfig
from flask import flash
from models import db
from models import Maestros
from models import Alumnos
from models import Pizzas
from datetime import datetime, date
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

@app.route("/addp", methods=["GET", "POST"])
def addp():
    addp_form = forms.PizzaForm(request.form)

    nombre = ''
    direccion = ''
    telefono = ''
    num = ''
    tamanio = ''
    ingredientes = ''
    subtotal = 0  

    if request.method == "POST":
        if addp_form.validate():
            nombre = addp_form.nombre.data
            direccion = addp_form.direccion.data
            telefono = addp_form.telefono.data
            num = addp_form.num.data
            tamanio = addp_form.tamanio.data
            ingredientes = ", ".join(addp_form.ingredientes.data)

            if tamanio == "chica":
                subtotal += 40 * num  
            elif tamanio == "mediana":
                subtotal += 80 * num 
            elif tamanio == "grande":
                subtotal += 120 * num 

            subtotal += 10 * len(addp_form.ingredientes.data) * num

            with open("pizza.txt", "a") as archivo:
                archivo.write(f"{nombre}-{direccion}-{telefono}-{num}-{tamanio}-{ingredientes}-{subtotal}\n")


            return redirect(url_for("addp"))

        elif "delete" in request.form:
            index = int(request.form["delete"])

            with open("pizza.txt", "r") as archivo:
                lineas = archivo.readlines()

            del lineas[index]

            with open("pizza.txt", "w") as archivo:
                archivo.writelines(lineas)

    with open("pizza.txt", "r") as archivo:
        lineas = archivo.readlines()
        datos = [linea.strip().split("-") for linea in lineas]


    total = sum(float(linea.split("-")[-1]) for linea in lineas)

    flash(f"Total de el Pedido: ${total}", "info")

    datos_con_indices = [(i, dato) for i, dato in enumerate(datos)]

    return render_template('pizza.html', form=addp_form, datos=datos_con_indices, nombre=nombre, direccion=direccion,
                            telefono=telefono, num=num, tamanio=tamanio, ingredientes=ingredientes, subtotal=subtotal)

@app.route("/confirmar_pedido", methods=["POST"])
def confirmar_pedido():

    with open("pizza.txt", "r") as archivo:
        lineas = archivo.readlines()

    for linea in lineas:
        datos = linea.strip().split("-")
        nombre, direccion, telefono, num, tamanio, ingredientes, subtotal = datos

        pizza = Pizzas(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            num=int(num),
            tamanio=tamanio,
            ingredientes=ingredientes,
            subtotal=float(subtotal),
            create_date=datetime.now()
        )
        db.session.add(pizza)

    db.session.commit()

    open("pizza.txt", "w").close()

    flash("¡Pedido registrado exitosamente!", "success")

    return redirect(url_for("addp"))

@app.route("/pedidos_del_dia")
def pedidos_del_dia():

    fecha_actual = date.today()

    pedidos = Pizzas.query.filter(Pizzas.create_date == fecha_actual).all()

    total_ventas = sum(pedido.subtotal for pedido in pedidos)

  
    return render_template("pedidosdeldia.html", pedidos=pedidos, total_ventas=total_ventas)

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