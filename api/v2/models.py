# Dependencias
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Base de datos
from .database import Base


class Jugador(Base):
    """ Modelo de usuario para la base de datos """
    __tablename__ = "jugadores"

    id_jugador = Column(String, primary_key=True, index=True, unique=True)
    fecha_creacion = Column(String, default=datetime.datetime.utcnow)
    fecha_ultima_partida = Column(String, default=None)

    items = relationship("Partida", back_populates="jugador")



class Partida(Base):
    """ Modelo de partida para la base de datos """
    __tablename__ = "partidas"

    id_partida = Column(String, primary_key=True, index=True, unique=True)
    talbero = Column(String, default=None)
    estado = Column(Integer, default=1)
    turno = Column(Integer, default=0)
    juega = Column(Integer, default=2)
    description = Column(String, index=True)
    id_jugador_1 = Column(String, ForeignKey("jugadores.id"))
    id_jugador_2 = Column(String, ForeignKey("jugadores.id"), default=None)
    fecha_creacion = Column(String, default=datetime.datetime.utcnow)
    fecha_ultima_actualizacion = Column(String, default=datetime.datetime.utcnow)
    tipo_de_partida = Column(Integer, default=None)

    jugador_1 = relationship("Jugador", back_populates="partidas")
