# api-othello

## v1 - PHP

Esta es la primera versión que estaba en desarrollo, de momento congelada.

## v2 - Python y fast api
Para poder ejecutar esta versión necesitamos seguir los siguientes pasos:

1. Creamos el entorno virtual de python dentro de la carpeta api

```` 
 python3 -m venv venv 
 ````

2. Iniciamos el entorno virtual
```` 
 source venv/bin/activate
 ````
Nota: si queremos desactivarlo usamos el siguiente comando:
```` 
 deactivate
 ````

3. Instalamos Fast api
```` 
pip3 install fastapi
 ````

4. Instalamos el servidor.
```` 
pip3 install uvicorn
 ````

5. Iniciamos el servidor
```` 
uvicorn v2.main:app --reload
 ````