import self
import db
from sqlalchemy import (Column, Integer, String, Boolean, DateTime)
from datetime import datetime, timedelta


class Categorias():
    """"Categorias:
        Es una clase para ser usada en Tarea()
        instanciada en main.py home()
            args
            trabajo : str trabajo
            hogar : str hogar
            estudio : str estudio"""

    def __init__(self, trabajo, hogar, estudio):
        self.trabajo = trabajo
        self.hogar = hogar
        self.estudio = estudio
        print("Categorias creadas con éxito")


    def __str__(self):
        return "Categorias: {}-- {}-- {}".format(self.trabajo, self.hogar, self.estudio)


class Tarea(db.Base):
    """Tarea:
       Esta clase representa tareas en general
            args
            id : autoincremental (PK)
            contenido : str texto de tarea
            categoria : str son posibles solo tres
            depende de la clase Categoria()
                . trabajo
                . hogar
                . estudio
            hecha : bool tarea lista o pendiente
            fecha : DateTime de sqlAlchemy"""
    __tablename__ = "tarea"
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    contenido = Column(String(200), nullable=False)
    categoria = Column(String(200), nullable=True)
    hecha = Column(Boolean)
    fecha = Column(DateTime, default=datetime.utcnow)

    def __init__(self, contenido, hecha, categoria, fecha):
        self.contenido = contenido
        self.hecha = hecha
        self.categoria = categoria
        self.fecha = fecha
        print("Tarea creada con éxito")

    # funcion para representacion por consola
    def __repr__(self):
        return "Tarea {}: {} ({}) {}".format(self.id, self.contenido, self.hecha, self.categoria, self.fecha)

    def __str__(self):
        return "Tarea {}: {} ({}) {} fecha: {}".format(self.id, self.contenido, self.hecha, self.categoria, self.fecha)
