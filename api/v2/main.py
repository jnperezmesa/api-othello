from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas, options
from .database import SessionLocal, engine

# Crea la base de datos
models.Base.metadata.create_all(bind=engine)

""" FAST API """
app = FastAPI()


""" BASE DE DATOS """
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

""" CONSTANTES """
URL_BASE_JUGADOR = "/api/v2/jugador/"
URL_BASE_PARTIDA = "/api/v2/partida/"


""" ENDPOINTS """
@app.get(str(f"{URL_BASE_PARTIDA}" + "{id_partida}"), response_model=schemas.VerPartida)
def ver_partida(id_partida, db: Session = Depends(get_db)):
    """ Comprobar el estado de la partida """
    # Buscamos la partida
    partida = crud.buscar_partida(db=db, id_partida=id_partida)
    # Comprobamos si hemos recuperado la partida
    if partida is None:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    else:
        # Nos aseguramos de que es la partida correcta
        if id_partida == partida.id_partida:
            # Preparamos la respuesta
            respuesta = schemas.VerPartida(
                estado=partida.estado,
                turno=partida.turno,
                juega=partida.juega,
                tablero=partida.tablero,
                fecha_ultima_actualizacion=partida.fecha_ultima_actualizacion,
            )
            # Entregamos la respuesta
            return respuesta
        else:
            raise HTTPException(status_code=404, detail="Partida incorrecta")


@app.post(f"{URL_BASE_JUGADOR}crear/", response_model=schemas.Jugador)
def crear_jugador(db: Session = Depends(get_db)):
    """ Crear un nuevo jugador y devolver el id """
    nuevo = crud.registrar_jugador(db=db)
    respuesta = schemas.Jugador(
        id_jugador=nuevo.id_jugador
    )
    return respuesta


@app.post((f"{URL_BASE_PARTIDA}crear/" + "{id_jugador}/{tipo_de_partida}/"), response_model=schemas.Partida)
def crear_partida(id_jugador, tipo_de_partida, db: Session = Depends(get_db)):
    """ Crear una nueva partida y devolver el id """
    crear = schemas.CrearPartida(
        id_jugador=id_jugador,
        tipo_de_partida=tipo_de_partida
    )
    nueva = crud.registrar_partida(db=db, datos=crear)
    respuesta = schemas.Partida(
        id_partida=nueva.id_partida,
    )
    return respuesta


@app.put(str(f"{URL_BASE_PARTIDA}unirse/" + "{id_partida}/{id_jugador}/"), response_model=schemas.VerPartida)
def unirse_a_partida(id_partida, id_jugador, db: Session = Depends(get_db)):
    """ Unirse a una partida """
    # Busca la partida
    partida = crud.buscar_partida(db, id_partida)
    datos = schemas.UnirseAPartida(
        id_partida=id_partida,
        id_jugador=id_jugador,
    )
    if partida.id_partida == id_partida:
        if partida.estado == options.Estado.espera:
            partida_actualizada = crud.registrar_jugador_2(db=db, datos=datos)
            respuesta = schemas.VerPartida(
                estado=partida_actualizada.estado,
                turno=partida_actualizada.turno,
                juega=partida_actualizada.juega,
                tablero=partida_actualizada.tablero,
                fecha_ultima_actualizacion=partida_actualizada.fecha_ultima_actualizacion,
            )
            return respuesta
        elif partida.estado == options.Estado.activa:
            raise HTTPException(status_code=400, detail="La partida está en curso")
        elif partida.estado == options.Estado.cerrada:
            raise HTTPException(status_code=400, detail="La partida ha terminado")
    else:
        raise HTTPException(status_code=404, detail="Código de partida incorrecto")
