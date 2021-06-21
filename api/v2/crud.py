from sqlalchemy.orm import Session
from . import models, schemas


#--------------------------------------------------------------------------------------------
# Jugadores
#--------------------------------------------------------------------------------------------
def buscar_jugador(db: Session, id_jugador: int):
    """ Función que busca a un jugador por su id """
    # Filtramos la base de datos en busca de una coincidencia
    return db.query(models.Jugador).filter(models.Jugador.id_jugador == id_jugador).first()


def registrar_jugador(db: Session, jugador: schemas.UserCreate):
    # Creo el id del jugador
    id_jugador = jugador.password + "notreallyhashed"
    if db.query(models.Jugador).filter(models.Jugador.id_jugador == id_jugador) > 0:
        # Relleno la ficha del jugador
        db_jugador = models.Jugador(
            id_jugador=id_jugador,
        )
        # Agrego la ficha del jugador a la base de datos
        db.add(db_jugador)
        # Guardo los cambios en la base de datos
        db.commit()
        # Actualizo los cambios en la base de datos
        db.refresh(db_jugador)
        # Deuelvo el id del jugador
        return db_jugador.id_jugador
    else:
        registrar_jugador(db, jugador)



#--------------------------------------------------------------------------------------------
# Partidas
#--------------------------------------------------------------------------------------------
def buscar_partida(db: Session, id_partida: int):
    """ Funcion que busca una partida por su id """
    # Filtramos la base de datos en busca de una coincidencia
    return db.query(models.Partida).filter(models.Partida.id_partida == id_partida).first()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
