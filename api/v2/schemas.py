from typing import List, Optional
from pydantic import BaseModel
from . import options


""" Modelos para ver """

class Jugador(BaseModel):
    """ Modelo para pedir el jugador """
    id_jugador: str


class Partida(BaseModel):
    """ Modelo para pedir la partida """
    id_partida: str


class EstadoPartida(BaseModel):
    """ Modelo para ver el estado de la partida """
    estado: int
    turno: int
    juega: int
    victoria: Optional[int] = None
    ficha_jugador_1: int
    capturas_jugador_1: int
    ficha_jugador_2: int
    capturas_jugador_2: int
    tablero: Optional[str] = None
    fecha_ultima_actualizacion: str


""" Modelos para modificar """

class CrearPartida(BaseModel):
    """ Modelo para crear la partida """
    tipo_de_partida: int
    id_jugador: str


class UnirseAPartida(BaseModel):
    """ Modelo para unirse a la partida """
    id_partida: str
    id_jugador: str


class ColocarFicha(BaseModel):
    """ Modelo para calcular el juego desde el servidor """
    turno: int
    pos_x: int
    pos_y: int
    ficha: int
    juega: options.Juega
    tablero: str
    fecha_ultima_actualizacion: str
