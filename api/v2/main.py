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
@app.get(str(f"{URL_BASE_PARTIDA}" + "{id_partida}"))
def ver_partida(id_partida, db: Session = Depends(get_db)):
    """ Comprobar el estado de la partida """
    partida = crud.buscar_partida(db=db, id_partida=id_partida)
    if partida is None:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    else:
        return partida


@app.post(f"{URL_BASE_JUGADOR}nuevo/", response_model=schemas.Jugador)
def crear_jugador(db: Session = Depends(get_db)):
    """ Crear un nuevo jugador y devolver el id """
    jugador = schemas.Jugador
    jugador.id_jugador = crud.registrar_jugador(db=db)
    return jugador


@app.post(f"{URL_BASE_PARTIDA}crear/", response_model=schemas.Partida)
def crear_partida(crear: schemas.CrearPartida, db: Session = Depends(get_db)):
    """ Crear una nueva partida y devolver el id """
    partida = crud.registrar_partida(db=db, peticion=crear)
    return partida


@app.put(str(f"{URL_BASE_PARTIDA}unirse/" + "{id_partida}/{id_jugador}/"), response_model=schemas.ActualizarPartida)
def unirse_a_partida(id_partida, id_jugador, db: Session = Depends(get_db)):
    """ Unirse a una partida """
    # Busca la partida
    partida = crud.buscar_partida(db, nuevo_jugador.id_partida)
    if partida.id_partida == nuevo_jugador.id_partida:
        if partida.estado == options.Estado.espera:
            crud.actualizar_partida(db=db, partida=partida)
            crud.actualizar_jugador(db=db, )
            return partida
        elif partida.estado == options.Estado.activa:
            raise HTTPException(status_code=400, detail="La partida está en curso")
        elif partida.estado == options.Estado.cerrada:
            raise HTTPException(status_code=400, detail="La partida ha terminado")
    else:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
