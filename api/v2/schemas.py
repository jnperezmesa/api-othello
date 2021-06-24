from typing import List, Optional
from pydantic import BaseModel
from . import options


class Jugador(BaseModel):
    """ Modelo para pedir el jugador """
    id_jugador: str


class Partida(BaseModel):
    """ Modelo para pedir la partida """
    id_partida: str


class VerPartida(BaseModel):
    """ Modelo para ver el estado de la partida """
    estado: int
    turno: int
    juega: int
    tablero: Optional[str] = None


class CrearPartida(BaseModel):
    """ Modelo para crear la partida """
    tipo_de_partida: int
    id_jugador: str


class UnirseAPartida(BaseModel):
    """ Modelo para unirse a la partida """
    id_partida: str
    id_jugador: str


class ActualizarPartida(BaseModel):
    """ Modelo para actualizar el tablero desde la aplicación o el servidor """
    id_partida: str
    id_jugador: str
    estado: options.Estado
    turno: int
    juega: options.Juega
    tablero: str


class ColocarFicha(BaseModel):
    """ Modelo para calcular el juego desde el servidor """
    id_partida: str
    id_jugador: str
    turno: int
    pos_x: int
    pos_y: int
    ficha: int
    juega: options.Juega
    tablero: str