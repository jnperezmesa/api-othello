# Dependencias
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from . import options

# Base de datos
from .database import Base


class Jugador(Base):
    """ Modelo de usuario para la base de datos """
    __tablename__ = "jugadores"

    id_jugador = Column(String, primary_key=True, index=True, unique=True)
    fecha_creacion = Column(String, default=str(datetime.now()))
    fecha_ultima_partida = Column(String, default=None)


class Partida(Base):
    """ Modelo de partida para la base de datos """
    __tablename__ = "partidas"

    id_partida = Column(String, primary_key=True, index=True, unique=True)
    tipo_de_partida = Column(Integer, default=None)

    tablero = Column(String, default=None)
    estado = Column(Integer, default=options.Estado.espera)
    turno = Column(Integer, default=0)
    juega = Column(Integer, default=options.Juega.negras)

    victoria = Column(Integer, default=None)

    id_jugador_1 = Column(String, default=None)
    ficha_jugador_1 = Column(Integer, default=options.Juega.negras)
    capturas_jugador_1 = Column(Integer, default=2)

    id_jugador_2 = Column(String, default=None)
    ficha_jugador_2 = Column(Integer, default=options.Juega.blancas)
    capturas_jugador_2 = Column(Integer, default=2)

    fecha_creacion = Column(String, default=str(datetime.now()))
    fecha_ultima_actualizacion = Column(String, default=str(datetime.now()))

