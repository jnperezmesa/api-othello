import string, random
from sqlalchemy import update


def generar_id(caracteres=4):
    """ Función que genera un alfanumérico aleatorio """
    # Array para almacenar los caracteres
    id_array = []
    # Bucle que genera un caracter en cada ciclo
    for caracter in range(caracteres):
        # Numero aleatorio que establece si será número o letra
        dado = random.randint(0, 9)
        # Si es menor que 5 entregará un numero
        if dado < 5:
            # Numero aleatorio
            caracter_aleatorio = str(random.randint(0, 9))
        # Si es mayor mayor o igual que 5 dará una letra
        else:
            # Letra aleatoria
            caracter_aleatorio = random.choice(string.ascii_letters)
        # Agrego el nuevo carácter
        id_array.append(caracter_aleatorio.upper())
    # Se pasa a string
    id = str(''.join(id_array))
    return id


def nuevo_turno(turno_actual):
    """ Función que suma el turno """
    nuevo_turno = int(turno_actual) + 1
    return nuevo_turno


def guardar_datos(db, registro):
    """ Funcion crea nuevos registros en la base de datos """
    # Agrega el nuevo registro a la base de datos
    db.add(registro)
    # Guarda los cambios en la base de datos
    db.commit()
    # Refresca la base de datos
    db.refresh(registro)
    # Devuelvo el registro que se ha guardado
    return registro
