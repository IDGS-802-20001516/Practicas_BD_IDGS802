from flask import Flask, request,render_template,Response,redirect,url_for
import forms
from flask_wtf.csrf import CSRFProtect
from flask import g 
from config import DevelopmentConfig
from flask import flash
from sqlalchemy import func
from models import db
from models import Maestros
from models import Alumnos
from models import Pizzas
from datetime import datetime, date
from datetime import datetime, timedelta
from flask import session

from collections import defaultdict

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
    fecha_pedido = ''  
    if request.method == "POST":
        if addp_form.validate():
            nombre = addp_form.nombre.data
            direccion = addp_form.direccion.data
            telefono = addp_form.telefono.data
            num = addp_form.num.data
            tamanio = addp_form.tamanio.data
            ingredientes = ", ".join(addp_form.ingredientes.data)
            fecha_pedido = addp_form.fecha.data  

            if tamanio == "chica":
                subtotal += 40 * num  
            elif tamanio == "mediana":
                subtotal += 80 * num 
            elif tamanio == "grande":
                subtotal += 120 * num 

            subtotal += 10 * len(addp_form.ingredientes.data) * num

            with open("pizza.txt", "a") as archivo:
                archivo.write(f"{nombre}@{direccion}@{telefono}@{num}@{tamanio}@{ingredientes}@{fecha_pedido}@{subtotal}\n")
            
    if request.method == "GET" and request.args.get("borrar"):
        indices_a_borrar = request.args.getlist("borrar")
        with open("pizza.txt", "r") as archivo:
            lineas = archivo.readlines()
        with open("pizza.txt", "w") as archivo:
            for i, linea in enumerate(lineas):
                if str(i) not in indices_a_borrar:
                    archivo.write(linea)

 
    with open("pizza.txt", "r") as archivo:
        lineas = archivo.readlines()
        if lineas:
            ultimo_pedido = lineas[-1].strip().split("@")
            nombre = ultimo_pedido[0]
            direccion = ultimo_pedido[1]
            telefono = ultimo_pedido[2]
            num = ultimo_pedido[3]
            tamanio = ultimo_pedido[4]
            ingredientes = ultimo_pedido[5]
            fecha_pedido = ultimo_pedido[6]
            print (fecha_pedido)
            subtotal = float(ultimo_pedido[7])

    with open("pizza.txt", "r") as archivo:
        lineas = archivo.readlines()
        datos = [linea.strip().split("@") for linea in lineas]

    datos_con_indices = [(i, dato) for i, dato in enumerate(datos)]

    total_pedidos = sum(float(dato[7]) for dato in datos)

    fecha_actual = date.today()
    pedidos = Pizzas.query.filter(func.DATE(Pizzas.fecha_registro_pedido) == fecha_actual).all()
    total_ventas = db.session.query(func.sum(Pizzas.subtotal)).filter(func.DATE(Pizzas.fecha_registro_pedido) == fecha_actual).scalar()

    return render_template('pizza.html', form=addp_form, datos=datos_con_indices, total_ventas=total_ventas, pedidos=pedidos, nombre=nombre, direccion=direccion,
                            telefono=telefono, num=num, tamanio=tamanio, ingredientes=ingredientes, subtotal=subtotal, total_pedidos=total_pedidos, fecha_pedido=fecha_pedido)
@app.route("/buscar_pedidos", methods=["GET", "POST"])
def buscar_pedidos():
    pedidos = []
    total_subtotal = 0

    if request.method == "POST":
        busqueda_dia = request.form.get("busqueda_dia")
        busqueda_mes = request.form.get("busqueda_mes")

        if busqueda_dia:
            if busqueda_dia.isdigit():
                dia_numero = int(busqueda_dia)
                if 1 <= dia_numero <= 7:
                    dia_index_sqlalchemy = dia_numero % 7 + 1
                    pedidos = Pizzas.query.filter(func.DAYOFWEEK(Pizzas.fecha_pedido) == dia_index_sqlalchemy).all()
            else:
                dias_semana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
                if any(busqueda_dia.lower() == d.lower() for d in dias_semana):
                    dia_index = dias_semana.index(next(d for d in dias_semana if d.lower() == busqueda_dia.lower())) + 1
                    dia_index_sqlalchemy = dia_index % 7 + 1
                    pedidos = Pizzas.query.filter(func.DAYOFWEEK(Pizzas.fecha_pedido) == dia_index_sqlalchemy).all()

        if busqueda_mes:
            if busqueda_mes.isdigit():
                mes_numero = int(busqueda_mes)
                if 1 <= mes_numero <= 12:
                    pedidos = Pizzas.query.filter(func.MONTH(Pizzas.fecha_pedido) == mes_numero).all()
            else:
                meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
                if any(busqueda_mes.lower() == m.lower() for m in meses):
                    mes_numero = meses.index(next(m for m in meses if m.lower() == busqueda_mes.lower())) + 1
                    pedidos = Pizzas.query.filter(func.MONTH(Pizzas.fecha_pedido) == mes_numero).all()

        pedidos = [{'nombre': pedido.nombre, 'subtotal': pedido.subtotal, 'fecha': pedido.fecha_pedido.strftime("%Y-%m-%d")} for pedido in pedidos]
        total_subtotal = sum(pedido['subtotal'] for pedido in pedidos)

    return render_template("buscar_pedidos.html", pedidos=pedidos, total_subtotal=total_subtotal)

@app.route("/deletep", methods=["POST"])
def deletep():
    selected_indices = request.form.get("selected_rows").split(",")

    with open("pizza.txt", "r") as archivo:
        lineas = archivo.readlines()

    for index in sorted(selected_indices, reverse=True):
        del lineas[int(index)]
    with open("pizza.txt", "w") as archivo:
        archivo.writelines(lineas)
    return redirect(url_for("addp"))

@app.route("/confirmar_pedido", methods=["POST"])
def confirmar_pedido():
    subtotal_total = 0
    fecha_pedido = None

    with open("pizza.txt", "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split("@")
            subtotal_total += float(datos[7])
            if fecha_pedido is None:
                fecha_pedido = datos[6]

    if subtotal_total > 0:
        with open("pizza.txt", "r") as archivo:
            primer_pedido = archivo.readline().strip().split("@")
            nombre = primer_pedido[0]

        pedido = Pizzas(
            nombre=nombre,
            fecha_pedido=fecha_pedido,
            subtotal=subtotal_total
        )
        db.session.add(pedido)
        db.session.commit()

        open("pizza.txt", "w").close()

        flash("¡Pedido registrado exitosamente!", "success")
    else:
        flash("No se encontraron pedidos para confirmar.", "warning")

    return redirect(url_for("addp"))
#ESTE COMIT LO HAGO POR QUE PUSE MAL LA DESCRIPCION DEL ANTERIOR COMIT PERO YA ESTA COMPLETO LA PRACTICA DE LA PIZZERIA 

@app.route("/pedidosdd", methods=["GET", "POST"])
def pedidosdd():
    fecha_actual = date.today()
    pedidos = Pizzas.query.filter(func.DATE(Pizzas.fecha) == fecha_actual).all()
    total_ventas = db.session.query(func.sum(Pizzas.subtotal)).filter(func.DATE(Pizzas.fecha) == fecha_actual).scalar()

    return render_template("pizza.html", pedidos=pedidos, total_ventas=total_ventas)



@app.route("/ABC_CompletoMestros", methods=["GET", "POST"])
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