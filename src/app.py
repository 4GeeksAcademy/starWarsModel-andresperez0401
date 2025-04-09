"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints, devuelve todas las rutas del sitio cuando se entra a la ruta principal
@app.route('/')
def sitemap():
    return generate_sitemap(app)



#-----------------------------------------Get Todas las Personas-----------------------------------------------------------------------------

@app.route('/people', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


#-----------------------------------------Get People por id-------------------------------------------------------------------------------------

@app.route('/people/<int:people_id>', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


#-----------------------------------------Get Todos los Planetas-----------------------------------------------------------------------------

@app.route('/planets', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



#-----------------------------------------Get Planet por id-------------------------------------------------------------------------------------

@app.route('/planet/<int:people_id>', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



#-----------------------------------------Get Todos los Usuarios-----------------------------------------------------------------------------

@app.route('/users', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



#-----------------------------------------Get Todos los Favoritos de un usuari0-----------------------------------------------------------------------------

@app.route('/users/favorites', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



#-----------------------------------------Agrega un planet favorito al usuario actual con el id: planet_id, tambien elimina-----------------------------------------------------------------------------

@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



#-----------------------------------------Agrega un people favorito al usuario actual con el id: people_id, tambien elimina-----------------------------------------------------------------------------

@app.route('/favorite/people/<int:people_id>', methods=['POST', 'DELETE'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200








#--------------------------------------------------------------------------------------------------------------------------------------------------
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
