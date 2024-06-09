from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

import db
from models import Tarea, Categorias

app = Flask(__name__)


@app.route('/')
def home():
    """def home():
        Obtiene todos los registros de la tabla Tareas de la base de datos,
        y luego renderiza el template principal.
    """
    alert = False
    todas_las_tareas = db.session.query(Tarea).all()
    categorias1 = Categorias("Trabajo", "Hogar", "Estudio")
    categorias_dic = categorias1.__dict__
    categorias = []
    for key, value in categorias_dic.items():
        categorias.append(value)
    return render_template("index.html",
                           lista_de_tareas=todas_las_tareas,
                           categorias=categorias,
                           datetime=datetime,
                           alert=alert)


@app.route('/crear-tarea', methods=["POST"])
def crear():
    """def crear():
        Crea los registros de la tabla Tareas en la base de datos,
        según el método "POST" que reciba como parámetro.
    """
    try:
        categoria_py = request.form.get("categoria")
        if categoria_py is None:
            raise ValueError("¡¡¡Falta marcar categoria!!!")

        fecha_str = request.form["fecha"]

        if fecha_str is None:
            raise ValueError("¿Falta marcar fecha!")

        print(f"Tipo de fecha_py: {type(fecha_str)}")
        fecha_py = datetime.strptime(fecha_str, '%Y-%m-%d')
        print(f"Tipo de fecha_py: {type(fecha_py)}")

        tarea = Tarea(contenido=request.form["contenido_tarea"].lower().title(),
                      categoria=categoria_py,
                      hecha=False,
                      fecha=fecha_py)
        db.session.add(tarea)
        db.session.commit()
    except ValueError as ve:
        alert = True
        print(f"Error: {ve}")
        db.session.rollback()
        return render_template('index.html',
                               alert=alert,
                               error_message=str(ve),
                               datetime=datetime)
    except Exception as e:
        alert = True
        db.session.rollback()
        print("Error en crear:", type(e).__name__)
        return render_template('index.html',
                               alert=alert,
                               error_message="Ha ocurrido un error inesperado.",
                               datetime=datetime)

    return redirect(url_for("home"))


@app.route('/volver')
def volver():
    """def volver():
        Esta función redirige a 'home()' si se activa la excepción en crear().
    """
    return redirect(url_for("home"))


@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    """def eliminar(id):
        Elimina tareas según el ID que reciba por parámetro."""
    try:
        tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
        if not tarea:
            raise ValueError(f"la tarea con id {id} no existe en la base de datos")
        db.session.delete(tarea)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error en eliminar: {type(e).__name__}")
        return render_template("index.html",
                               alert=True,
                               datetime=datetime)
    return redirect(url_for("home"))


@app.route('/tarea-hecha/<id>')
def editar(id):
    """def editar(id):
        Edita tareas según el ID que reciba por parámetro,
        modificando el atributo 'hecha'."""
    try:
        print("Se recibió id:", id)
        tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
        if not tarea:
            raise ValueError(f"la tarea con id {id} no existe en la base de datos")
        print("Se buscó en db tarea: ", tarea)
        tarea.hecha = not tarea.hecha
        print("Tarea hecha:", tarea.hecha)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error en editar: {type(e).__name__}")
        return render_template("index.html",
                               alert=True,
                               datetime=datetime)
    return redirect(url_for("home"))


@app.route("/editar-contenido", methods=["POST"])
def activar_section_contenido():
    """def activar_section_contenido():
        Captura la tarea cuyo contenido se desea modificar,
        y redirige a contenido.html."""
    try:
        tarea_id = request.form["tarea_id"]
        tarea = db.session.query(Tarea).filter_by(id=int(tarea_id)).first()
        if not tarea:
            raise ValueError(f"la tarea con id {tarea_id} no existe en la base de datos")
    except Exception as e:
        db.session.rollback()
        print(f"Error en editar-contenido: {type(e).__name__}")
        return render_template("index.html",
                               datetime=datetime)

    return render_template("contenido.html", tarea=tarea, datetime=datetime)


@app.route('/edicion-contenido', methods=["POST"])
def editar_contenido():
    """def editar_contenido():
        Modifica:  tarea.contenido y/o tarea.fecha,
        luego redirige a home."""
    try:
        tarea_id = request.form["tarea_id"]
        tarea = db.session.query(Tarea).filter_by(id=int(tarea_id)).first()
        tarea.contenido = request.form["nuevo_contenido_tarea"]
        fecha_str = request.form["fecha"]
        fecha_py = datetime.strptime(fecha_str, '%Y-%m-%d')
        tarea.fecha = fecha_py
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error en editar: {type(e).__name__}")

    return redirect(url_for("home"))


@app.route('/filtro-categoria', methods=["POST"])
def filtro_categoria():
    """def filtro_categoria():
        Esta función filtra las tareas por categoria,
        puede redirigir según corresponda hacia:
        hogar.html
        trabajo.html
        estudio.html.
    """
    try:
        todas_las_tareas = db.session.query(Tarea).all()
        tarea_hogar = []
        tarea_trabajo = []
        tarea_estudio = []
        categoria_py = request.form.get("categoria-en-footer")
        print("categoria que llega de footer", categoria_py)
        for tarea in todas_las_tareas:
            if categoria_py == "Hogar" and tarea.categoria == categoria_py and not tarea.hecha:
                tarea_hogar.append(tarea)
                print(tarea_hogar)
            elif categoria_py == "Trabajo" and tarea.categoria == categoria_py and not tarea.hecha:
                tarea_trabajo.append(tarea)
                print(tarea_trabajo)
            elif categoria_py == "Estudio" and tarea.categoria == categoria_py and not tarea.hecha:
                tarea_estudio.append(tarea)
                print(tarea_estudio)

    except Exception as e:
        print(f"Error en filtro_categoria(): {type(e).__name__}")
        return redirect(url_for("home"))

    if categoria_py == "Hogar":
        return render_template("hogar.html", tarea_hogar=tarea_hogar, datetime=datetime)
    elif categoria_py == "Trabajo":
        return render_template("trabajo.html", tarea_trabajo=tarea_trabajo, datetime=datetime)
    elif categoria_py == "Estudio":
        return render_template("estudio.html", tarea_estudio=tarea_estudio, datetime=datetime)

if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)  # crea las tablas de todos los modelos
    app.run(debug=True)  # instruccion que va al final
