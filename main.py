from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash
import jwt
from functools import wraps
import controller
import connection
app = Flask(__name__)
ADMIN = 1
LEADER = 2
app.config['SECRET_KEY'] = 'Someverysecretshhh'
DB = connection.connection()


def token_validation(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'error': 'Token no encontrado'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # validate user
            user = {"role": data['role'], "user_id": data["user_id"]}

        except jwt.exceptions.ExpiredSignature:
            return jsonify({'error': 'Token Expirado'})
        except jwt.exceptions.InvalidSignatureError as err:
            return jsonify({'error': "{}".format(err)})
        # TODO: Should i handle more jwt.exceptions?
        return f(user, *args, **kwargs)
    return decorador


@app.route('/login', methods=["POST"])
def login():
    login_info = request.get_json()
    if login_info is None:
        return jsonify({"error": "Uso incorrecto del API"})
    if "documento" not in login_info or "contraseña" not in login_info:
        return jsonify({"error": "documento o contraseña no encontrada"})
    token = controller.get_user(login_info, app)
    return jsonify(token)


@app.route('/agregar_lider', methods=['POST', 'GET'])
@token_validation
def add_leader(user):
    print(request.files)
    data = request.get_json()
    if data is None:
        return jsonify({"error": "formato incorrecto"})
    if user["role"] != ADMIN:
        return jsonify({"error": "No tiene acceso para agregar lideres"})
    if "contrasenia" not in data:
        return "{'mensaje':'Agregue contraseña'}"
    data['contrasenia'] = generate_password_hash(
            data['contrasenia'], method='sha256')

    ubicacion_id = controller.get_location(data['direccion'], data)
    if "error" in ubicacion_id:
        return jsonify(ubicacion_id)

    data["privilegio_id"] = LEADER
    leader_id = controller.save_leader(data)

    if leader_id["status"] == -1:
        return jsonify({"error": "{}".format(leader_id["error_message"])})

    return jsonify({"status": "OK", "leader_id": leader_id["last_id"]})


@app.route('/votantes/<opt>', methods=['POST'])
@token_validation
def handle_voter_stats(user, opt):
    print("user", user)
    if user["role"] == ADMIN:
        if opt == "list":
            querystr = controller.get_all_count_data("usuario")
            rows = controller.fetch_voter_info(querystr)
            return jsonify(rows)
    if user["role"] == LEADER:
        if opt == "list":
            querystr = controller.get_all_leader_count_data(user)
            rows = controller.fetch_voter_info(querystr)
            return jsonify(rows)

    if opt == "lider_info":
        querystr = controller.get_all_voters_by_leaders(user)
        rows = controller.fetch_voter_info(querystr)
        return jsonify(rows)
    if opt == "municipio_info":
        querystr = controller.get_voter_by_municipality(user)
        rows = controller.fetch_voter_info(querystr)
        return jsonify(rows)
    if opt == "mesa_votacion_info":
        querystr = controller.get_voter_by_spot(user)
        rows = controller.fetch_voter_info(querystr)
        return jsonify(rows)

    return jsonify({"wait": "WIP"})


@app.route('/<table_name>/<opt>', methods=["POST"])
@token_validation
def handle_insert(user, table_name, opt):
    if request.method == "GET":
        return jsonify({"error": "metodo no autorizado"})
    # if role != LEADER:
    #    return jsonify({"error": "Sin autorizacion"})
    data = request.get_json()
    if opt == "agregar":
        if table_name == "votante":
            data["usuario_id"] = user["user_id"]
        if table_name == "mesa_votacion":
            ubicacion_id = controller.get_location(data['direccion'], data)
            if "error" in ubicacion_id:
                return ubicacion_id['error']

        status_query = controller.save_in_table(table_name, data)
        # print("stat", status_query)
        if status_query['status'] == -1:
            response = {
                "status": "FAIL",
                table_name+"_id": status_query['status'],
                "mensaje": status_query['error_message']
            }
            return jsonify(response)
        response = {
            "status": "OK",
            table_name+"_id": status_query["last_id"]
        }
        return jsonify(response)
    elif opt == "actualizar":
        return jsonify({"wait": "WIP"})
    elif opt == "eliminar":
        return jsonify({"wait": "WIP"})
    elif opt == "consultar":
        return jsonify({"wait": "WIP"})
    else:
        return jsonify({"error": "Funcion no soportanda"})


@app.route('/pong')
@app.route('/')
def ping():
    return "pong"


if __name__ == '__main__':
    app.run(host='0.0.0.0')


# https://www.geeksforgeeks.org/types-of-inheritance-python/
# https://developers.google.com/maps/documentation/geocoding/start?hl=es
# https://www.geeksforgeeks.org/python-functools-wraps-function/
# https://geekflare.com/es/securing-flask-api-with-jwt/ --
# https://github.com/Rev0kz/Flask-API-Token/blob/master/app.py --
# https://j2logo.com/tutorial-flask-leccion-5-base-de-datos-con-flask-sqlalchemy/
