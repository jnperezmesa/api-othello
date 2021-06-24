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
URL_BASE_JUGADOR = "/api/v2/jugador"
URL_BASE_PARTIDA = "/api/v2/partida"


""" ENDPOINTS """
@app.post(f"{URL_BASE_JUGADOR}/nuevo/")
def crear_jugador(db: Session = Depends(get_db)):
    return crud.registrar_jugador(db=db)


@app.post(f"{URL_BASE_PARTIDA}/crear/", response_model=schemas.CrearPartida)
def crear_partida(jugador_y_tipo: schemas.CrearPartida, db: Session = Depends(get_db)):
    partida = crud.registrar_partida(db=db, peticion=jugador_y_tipo)
    return partida

"""
@app.put(f"{URL_BASE_PARTIDA}/unirse/", response_model=schemas.UnirseAPartida)
def unirse_a_partida(nuevo_jugador: schemas.UnirseAPartida, db: Session = Depends(get_db)):
    # Busca la partida
    partida = crud.buscar_partida(db, nuevo_jugador.id_partida)
    if partida.id_partida == nuevo_jugador.id_partida:
        if partida.estado == options.Estado.espera:
            crud.actualizar_partida(db=db, partida=partida)
            crud.actualizar_jugador(db=db, )
            return partida
        elif partida.estado == options.Estado.activa:
            raise HTTPException(status_code=404, detail="La partida está en curso")
        elif partida.estado == options.Estado.cerrada:
            raise HTTPException(status_code=404, detail="La partida ha terminado")
    else:
        raise HTTPException(status_code=404, detail="Partida no encontrada")


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items




"""