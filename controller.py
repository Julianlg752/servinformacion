import connection
import geocoding
import mysql
from werkzeug.security import check_password_hash
import jwt
import datetime
ADMIN = 1
LEADER = 2


def getHeadersAndValues(struct):
    headers = []
    values = []
    for k, v in struct.items():
        headers.append(k)
        values.append(str(v))
    return headers, values


def insert(table_name, headers, values):
    return "insert into {} ({}) \
values('{}')".format(table_name, ",".join(headers), "','".join(values))


def select(table_name, headers):
    return format("select %s from %s" % (headers, table_name))


def selectwhere(table_name, headers, where):
    return format("select %s from %s where documento='%s'" %
                  (headers, table_name, where))


def get_clause(user):
    where_clause = ""
    if user["role"] != ADMIN:
        where_clause = "and votante.usuario_id = {}\
                ".format(str(user["user_id"]))
    return where_clause


# only Admin
def get_all_count_data(table_name):
    return "select count(*) as total_votantes from {}".format(table_name)


def get_all_leader_count_data(user):
    return "select count(*) as total_votantes, usuario.nombre \
            from votante, usuario \
            where votante.usuario_id=usuario.id \
            and votante.usuario_id = {}".format(str(user["user_id"]))


def get_all_voters_by_leaders(user):
    return "select count(*) total_votantes, \
            concat(usuario.nombre,' ',usuario.apellido) as nombre \
            from votante, usuario \
            where votante.usuario_id=usuario.id {where_clause}\
            group by usuario_id".format(where_clause=get_clause(user))


def get_voter_by_municipality(user):
    return "select count(*) as total_votantes, municipio.nombre  as municipio \
            from votante, municipio \
            where votante.municipio_id=municipio.id {where_clause} \
            group by municipio_id".format(where_clause=get_clause(user))


def get_voter_by_spot(user):
    return "select count(*) as total_votantes, \
            mesa_votacion.nombre as mesa_votacion \
            from votante, mesa_votacion \
            where votante.mesa_votacion_id=mesa_votacion.id {where_clause} \
            group by \
            votante.mesa_votacion_id".format(where_clause=get_clause(user))


def fetch_voter_info(querystr):
    rows = fetchall(querystr)
    if len(rows) < 1:
        return {"alerta": "No se encontraron registros"}
    return rows[0]


def get_user(login_info, app):
    # TODO: Improve this!
    columns = "id, privilegio_id, contrasenia"
    querystr = selectwhere("usuario", columns, login_info['documento'])
    rows = fetchall(querystr)
    token_life = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    for row in rows:
        # print("what", row[0]['contrasenia'])
        passwd = row[0]['contrasenia']
        if check_password_hash(passwd, login_info['contraseña']):
            payload = {
                "role": row[0]['privilegio_id'],
                "user_id": row[0]['id'],
                "exp": token_life
            }
            token = jwt.encode(payload, app.config['SECRET_KEY'])
            return {"token": token.decode('UTF-8')}
        else:
            return {"error": "Contraseña invalida"}


def get_location(address, data):
    response = {}
    response_geocoding = geocoding.get_lat_lon(address)
    if "error" in response_geocoding:
        response = {
                "error": "Intente de nuevo, direccion no encontrada"
                }
        return response

    ubicacion_id = add_location(response_geocoding)
    if ubicacion_id == -1:
        response = {
                "error": "No fue posible guardar la direccion"
                }
        return response
    data["ubicacion_id"] = str(ubicacion_id)
    return data


def save_in_table(table_name, data):
    headers, values = getHeadersAndValues(data)
    querystr = insert(table_name, headers, values)
    last_id, err = runQuery(querystr)
    if err != 1:
        print("Error inserting "+table_name+" [ERR01]: ", err)
        return {"status": -1, "error_message": err}
    return {"status": 1, "last_id": last_id.lastrowid}


# TODO: Change error handling, return a dict: status done!
def save_leader(data):
    headers, values = getHeadersAndValues(data)
    querystr = insert("usuario", headers, values)
    last_id, err = runQuery(querystr)
    if err != 1:
        print("Error inserting leader [ERR01]: ", err)
        return {"status": -1, "error_message": err}
    return {"status": 1, "last_id": last_id.lastrowid}


def add_location(location_dict):
    headers, values = getHeadersAndValues(location_dict)
    querystr = insert("ubicacion", headers, values)
    last_id, err = runQuery(querystr)
    if err != 1:
        print("Error inserting product [ERR02]: ", err)
        return -1
    return last_id.lastrowid


def runQuery(querystr):
    db = connection.connection()
    cursor = db.cursor()
    try:
        cursor.execute(querystr)
        db.commit()
    except mysql.connector.errors.IntegrityError as err:
        cursor.close()
        db.close()
        return -1, err.msg
    except mysql.connector.errors.DatabaseError as dbError:
        cursor.close()
        db.close()
        return -1, dbError.msg
    db.close()
    return cursor, 1


def fetchall(querystr):
    db = connection.connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(querystr)
        data = cursor.fetchall()
    except mysql.connector.errors.IntegrityError as err:
        cursor.close()
        db.close()
        return err.msg, -1

    db.close()
    return data, 1
