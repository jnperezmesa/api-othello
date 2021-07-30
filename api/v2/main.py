# Minimo fast api
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
# Para configurar los cors
from fastapi.middleware.cors import CORSMiddleware

from . import crud, models, schemas, options
from .database import SessionLocal, engine

# Crea la base de datos
models.Base.metadata.create_all(bind=engine)

""" FAST API """
app = FastAPI()

""" CORS """
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# BASE DE DATOS
def get_db():
    """Función que conecta la base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CONSTANTES
URL_BASE = "/api/v2/"
URL_BASE_JUGADOR = f"{URL_BASE}jugador/"
URL_BASE_PARTIDA = f"{URL_BASE}partida/"


@app.get(f"{URL_BASE}ping/")
def ping():
    return schemas.Pong()


# ENDPOINTS
@app.get(str(f"{URL_BASE_PARTIDA}" + "{id_partida}"), response_model=schemas.EstadoPartida)
def ver_partida(id_partida, db: Session = Depends(get_db)):
    """ Comprobar el estado de la partida o ver como espectador """
    # Buscamos la partida
    partida = crud.buscar_partida(db=db, id_partida=id_partida)
    # Comprobamos si hemos recuperado la partida
    if partida is None:
        raise HTTPException(status_code=404, detail="La partida no existe")
    else:
        # Nos aseguramos de que es la partida correcta
        if id_partida == partida.id_partida:
            # Preparamos la respuesta
            respuesta = schemas.EstadoPartida(
                estado=partida.estado,
                turno=partida.turno,
                juega=partida.juega,
                victoria=partida.victoria,
                tablero=partida.tablero,
                fecha_ultima_actualizacion=partida.fecha_ultima_actualizacion,
            )
            # Entregamos la respuesta
            return respuesta
        else:
            raise HTTPException(status_code=403, detail="El codigo no ha llegado bien")


@app.post(f"{URL_BASE_JUGADOR}crear/", response_model=schemas.Jugador, status_code=201)
def crear_jugador(db: Session = Depends(get_db)):
    """ Crear un nuevo jugador y devolver el id """
    # Registramos al nuevo jugador
    nuevo = crud.registrar_jugador(db=db)
    # Cargamos la respuesta
    respuesta = schemas.Jugador(
        id_jugador=nuevo.id_jugador
    )
    return respuesta


@app.post((f"{URL_BASE_PARTIDA}crear/" + "{tipo_de_partida}/{id_jugador}/"), response_model=schemas.Partida, status_code=201)
def crear_partida(id_jugador, tipo_de_partida, db: Session = Depends(get_db)):
    """ Crear una nueva partida y devolver el id """
    # Compruebo que es un jugador registrado
    if crud.buscar_jugador(db=db, id_jugador=id_jugador):
        # Preparamos los datos
        crear = schemas.CrearPartida(
            id_jugador=id_jugador,
            tipo_de_partida=tipo_de_partida
        )
        # Registramos la partida
        nueva = crud.registrar_partida(db=db, datos=crear)
        # Cargamos la respuesta
        respuesta = schemas.Partida(
            id_partida=nueva.id_partida,
            fecha_ultima_actualizacion=nueva.fecha_ultima_actualizacion,
        )
        return respuesta
    else:
        raise HTTPException(status_code=403, detail="No estás registrado")


@app.put(str(f"{URL_BASE_PARTIDA}unirse/" + "{id_partida}/{id_jugador}/"), response_model=schemas.EstadoPartida, status_code=202)
def unirse_a_partida(id_partida, id_jugador, db: Session = Depends(get_db)):
    """ Unirse a una partida existente y devolver el estado de la partida """
    # Busca la partida
    partida = crud.buscar_partida(db, id_partida)
    if crud.buscar_jugador(db=db, id_jugador=id_jugador):
        # Peparamos los datos
        datos = schemas.UnirseAPartida(
            id_partida=id_partida,
            id_jugador=id_jugador,
        )
        # Verificamos que el id es correcto
        if partida.id_partida == id_partida:
            # Comprobamos el estado de la partida
            if partida.estado == options.Estado.espera:
                # Si está en espera, guardamos los datos del nuevo jugador
                partida_actualizada = crud.registrar_jugador_2(db=db, datos=datos)
                # Cargamos el nuevo estado de la partida
                respuesta = schemas.EstadoPartida(
                    estado=partida_actualizada.estado,
                    turno=partida_actualizada.turno,
                    juega=partida_actualizada.juega,
                    victoria=partida_actualizada.victoria,
                    tablero=partida_actualizada.tablero,
                    fecha_ultima_actualizacion=partida_actualizada.fecha_ultima_actualizacion,
                )
                return respuesta
            elif partida.estado == options.Estado.activa:
                raise HTTPException(status_code=403, detail="Has llegado tarde, la partida ya ha empezado")
            elif partida.estado == options.Estado.cerrada:
                raise HTTPException(status_code=403, detail="Has llegado muy tarde, la partida ha terminado")
        else:
            raise HTTPException(status_code=404, detail="Te has equivocado de codigo")
    else:
        raise HTTPException(status_code=403, detail="No estás registrado")


@app.put(str(f"{URL_BASE_PARTIDA}jugar/" + "{id_partida}/{id_jugador}/"), response_model=schemas.EstadoPartida, status_code=202)
def jugar_turno(id_partida, id_jugador, movimiento: schemas.EstadoPartida, db: Session = Depends(get_db)):
    """ Jugar el turno enviando los datos desde la app y recibir el nuevo estado de la partida """
    # Busca la partida
    partida = crud.buscar_partida(db, id_partida)
    if partida.id_partida == id_partida:
        # Busca comprueba que el jugador es valido
        if partida.id_jugador_1 == id_jugador or partida.id_jugador_2 == id_jugador:
            # Compruebo que la partida está activa
            if partida.estado == options.Estado.activa:
                # Actualizamos el estado de la partida
                partida_actualizada = crud.actualizar_partida(db=db, id_jugador=id_jugador, id_partida=id_partida,
                                                              partida=movimiento)
                # Cargamos la respuesta con el nuevo estado de la partida
                respuesta = schemas.EstadoPartida(
                    estado=partida_actualizada.estado,
                    turno=partida_actualizada.turno,
                    juega=partida_actualizada.juega,
                    victoria=partida_actualizada.victoria,
                    tablero=partida_actualizada.tablero,
                    contador_jugador_1=partida_actualizada.contador_jugador_1,
                    contador_jugador_2=partida_actualizada.contador_jugador_2,
                    fecha_ultima_actualizacion=partida_actualizada.fecha_ultima_actualizacion,
                )
                return respuesta
            # Si no está activa le entrego la partida acabada
            else:
                sin_cambios = schemas.EstadoPartida(
                    estado=partida.estado,
                    turno=partida.turno,
                    juega=partida.juega,
                    victoria=partida.victoria,
                    tablero=partida.tablero,
                    contador_jugador_1=partida.contador_jugador_1,
                    contador_jugador_2=partida.contador_jugador_2,
                    fecha_ultima_actualizacion=partida.fecha_ultima_actualizacion,
                )
                return sin_cambios
        elif crud.buscar_jugador(db=db, id_jugador=id_jugador):
            raise HTTPException(status_code=403, detail="No juegas en esta partida")
        else:
            raise HTTPException(status_code=404, detail="No estás registrado")
    else:
        raise HTTPException(status_code=404, detail="Te has equivocado de codigo")


@app.put(str(f"{URL_BASE_PARTIDA}revancha/" + "{id_partida}/{id_jugador}/"), response_model=schemas.Partida, status_code=201)
def jugar_revancha(id_partida, id_jugador, db: Session = Depends(get_db)):
    # Busca la partida antigua
    partida = crud.buscar_partida(db, id_partida)
    if partida:
        # Compruebo que el jugador existe en mi base de datos
        if crud.buscar_jugador(db=db, id_jugador=id_jugador):
            # Si no existe id de la nueva partida lo creo
            if not partida.nueva_partida:
                # Preparamos los datos
                crear = schemas.CrearPartida(
                    id_jugador=id_jugador,
                    tipo_de_partida=tipo_de_partida
                )
                # Registramos la partida
                nueva = crud.registrar_partida_revancha(db=db, datos=crear, partida_antigua=partida)
                # Cargamos la respuesta
                respuesta = schemas.Partida(
                    id_partida=nueva.id_partida,
                    fecha_ultima_actualizacion=nueva.fecha_ultima_actualizacion,
                )
                return respuesta
            # Si existe id de la nueva partida lo entrego
            else:
                # Busco la partida
                nueva = crud.buscar_partida(db, partida.nueva_partida)
                # Preparo los datos
                datos = schemas.UnirseAPartida(
                    id_partida=nueva.id_partida,
                    id_jugador=id_jugador,
                )
                # Guardo al jugador nuevo
                crud.registrar_jugador_2(db=db, datos=datos)
                # La entrego
                respuesta = schemas.Partida(
                    id_partida=nueva.id_partida,
                    fecha_ultima_actualizacion=nueva.fecha_ultima_actualizacion,
                )
                return respuesta
        else:
            raise HTTPException(status_code=404, detail="No estás registrado")
    else:
        raise HTTPException(status_code=404, detail="Te has equivocado de codigo")