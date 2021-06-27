from enum import Enum

class Estado(int, Enum):
    """ Estado de la partida """
    activa = 1
    espera = 2
    cerrada = 3


class Juega(int, Enum):
    """ Fichas de juego """
    negras = 2
    blancas = 1


class Tipo(int, Enum):
    """ Tipo de partida """
    online = 1
    local = 2
    boot = 3