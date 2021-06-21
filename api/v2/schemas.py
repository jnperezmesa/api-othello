# Dependencias
from typing import List, Optional
from pydantic import BaseModel


# Jugador
class JugadorBase(BaseModel):
    id_jugador: str


class UserCreate(UserBase):
    password: str



class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


# Partida
class PartidaBase(BaseModel):
    title: str
    description: Optional[str] = None




class ItemCreate(ItemBase):
    pass



class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
