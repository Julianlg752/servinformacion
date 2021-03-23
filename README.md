# Servinformacion prueba

Pasos para ejecutar el servicio API de registro de votantes

La version de Python y pip en la cual se desarrollo esta prueba:
- Python 3.8.5
- pip 20.0.2

Ahora para instalar las dependencias ejecutar el siguiente comando:

```.sh
pip install -r requirements.txt
```
En el folder de las fuentes incluye un script de bash el cual contiene las variables de entorno para inicial el servidor de Flask, al ejecutarlo empezara a escuchar peticiones.

```.sh
./run.sh
```
# Base de Datos
La base de datos usada es de MySql version:
- mysql  Ver 8.0.23

En la carpeta /db existe un script de mysql el cual crea la base de datos, las tablas, agrega los privilegios o roles, y crea un usuario ADMIN con contraseña "some"
puede ver el [Modelo Base Datos](./db/modelo_db.png)

# Endpoints

## /login
Este endpoint recibe por metodo post un JSON el cual contiene dos campos:
- documento
- contraseña
Los cuales si son correctos retornara una llave de token JWT el cual se podra usar para ejecutar los diferentes llamados de API

```.sh
curl --location --request POST 'localhost:5000/login' --header 'Content-Type: application/json' \ 
--data-raw '{"documento":90210, "contraseña":"some"}'
```


## /agregar_lider
Este endpoint esta definido para agregar un lider, solo el usuario ADMIN puede hacer el registro de nuevos lideres.
```.sh
curl --location --request POST 'localhost:5000/agregar_lider' \
--header 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoxLCJ1c2VyX2lkIjoxLCJleHAiOjE2MTU3NjkzNDl9.agJcKWHkpzkROvee1PMKFX8udLJkchCPGlvj8bU7XBE' \
--data-binary '/home/jl/Downloads/2021.jpg' \
--header 'Content-Type: application/json' \
--data-raw '{
    "nombre":"jose",
    "apellido":"alvarado",
    "direccion":"Calle 145 #103b-55",
    "ciudad":"bogota",
    "celular":"90909090",
    "foto":"something",
    "contrasenia": "some",
    "tipo_documento":"cc",
    "documento":"123123123"
}'
```
## /table_name/opt
Este es un endpoint "generico" el cual se usa para agregar 
- departamentos
- municipios
- mesa_votacion
- votante

El primer parametro de la url hace referencia a cual de los anteriores quiere ejecutar una accion del CRUD, y el segundo parametro es para indicar la acción que puede ser:

- agregar (Hecha)
- actualizar (WIP)
- eliminar (WIP)
- consultar (WIP)

Puede ver el archivo con ejemplos [curl.txt](./curl.txt)
El cual contiene ejemplos de uso del endpoint

## /votantes/opt
Este endpoint sirve para obtener información de total de votantes creados:
- total inscritos en el sistema(Solo ADMIN)
- total inscritos por lider
- total inscritos por municipio
- total inscritos por mesa de votación

y el llamado es por medio de los siguientes "opt":
- list
- lider_info
- municipio_info
- mesa_votacion_info

Todas las peticiones excepto por la del login, requieren que se incluya el token de JWT en su request

Adicionalmente puede exportar la collecion de [Postman](./Servinformacion.postman_collection.json) la cual tiene la declaración de los endpoints
