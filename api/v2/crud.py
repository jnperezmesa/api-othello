from sqlalchemy.orm import Session
from . import models, schemas, tools


def buscar_jugador(db: Session, id_jugador):
    """ Función que busca a un jugador por su id """
    # Filtramos la base de datos en busca de una coincidencia
    return db.query(models.Jugador).filter(models.Jugador.id_jugador == id_jugador).first()


def buscar_partida(db: Session, id_partida):
    """ Funcion que busca una partida por su id """
    # Filtramos la base de datos en busca de una coincidencia
    return db.query(models.Partida).filter(models.Partida.id_partida == id_partida).first()


def registrar_jugador(db: Session):
    """ Función que registra a un jugador """
    # Creo el id del jugador
    id_jugador = tools.generar_id(caracteres=7)
    # Relleno la ficha del jugador
    db_jugador = models.Jugador(
        id_jugador=id_jugador,
    )
    # Agrego la ficha del jugador a la base de datos
    jugador = tools.guardar_datos(db=db, registro=db_jugador)
    # Devuelvo el id del jugador
    return jugador


def registrar_partida(db: Session, peticion: schemas.CrearPartida):
    """ Función que registra una partida """
    # Creo el id de la partida
    id = tools.generar_id()
    # Relleno la ficha de la partida
    db_partida = models.Partida(
        id_partida=id,
        id_jugador_1=peticion.id_jugador,
        tipo_de_partida=peticion.tipo_de_partida,
    )
    # Guardo los cambios y devuelvo el resultado
    partida = tools.guardar_datos(db=db, registro=db_partida)
    return partida

def actualizar_jugador_2(db: Session, peticion: schemas.UnirseAPartida):
    """ Función que agrega al jugador 2 a la partida"""
    pass


def actualizar_jugador(db: Session, id_jugador, fecha):
    """ Función que actualiza los datos del jugador """
    # Actualizo la fecha y hora de la última partida del jugador
    db_jugador = db.query(models.Partida).filter(models.Partida.id_jugador == id_jugador).update(
        {
            "fecha_ultima_partida": fecha
        }
    )
    # Guardo los datos
    db.commit()
    # Refresco la sesión
    db.refresh(db_jugador)
    # Compruebo si se han hecho los cambios
    if buscar_jugador(db, id_jugador=id_jugador).fecha_ultima_partida == fecha:
        return True
    else:
        return False


def actualizar_partida(db: Session, partida: schemas.ActualizarPartida):
    """ Función que actualiza el estado de la partida """
    # Actualizo la fecha y hora de la última partida del jugador
    fecha = datetime.datetime.utcnow
    db_partida = db.query(models.Partida).filter(models.Partida.id_partida == partida.id_partida).update(
        {
            "turno": tools.nuevo_turno(turno_actual=models.Partida.turno),
            "juega": partida.juega,
            "tablero": partida.tablero,
            "fecha_ultima_actualizacion": fecha,
        }
    )
    # Guardo los datos
    db.commit()
    # Refresco la sesión
    db.refresh(db_partida)
    # Compruebo que se han guardado los cambios
    if buscar_partida(db, id_partida=partida.id_partida).fecha_ultima_actualizacion == fecha:
        return db_partida
    else:
        return False
