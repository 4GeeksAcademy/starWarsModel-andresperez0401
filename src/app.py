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
from models import db, User, Character, Planet, Favorite

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


# with app.app_context():
#     char = Character()
#     char.id_character = 54
#     char.name = "andyJose"

#     db.session.add(char)
#     db.session.commit()

# -----------------------------------------Get Todas las Personas-----------------------------------------------------------------------------


@app.route('/people', methods=['GET'])
def get_all_people():

    all_people = Character.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    # Otra alternativa para serializar, cuando se consulta al modelo no se pude transformar directamente a un json, por eso se serializa
    # all_people = [person.serialize() for person in Person.query.all()]

    if all_people is None:
        response_body = {
            "msg": "Not people found"
        }
        return jsonify(response_body), 404

    return jsonify(all_people), 200


# -----------------------------------------Get People por id-------------------------------------------------------------------------------------

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):

    people = Character.query.get(people_id)

    if people is None:
        response_body = {
            "msg": "Not people with id: {" + str(people_id) + "} found"
        }
        return jsonify(response_body), 404

    people = people.serialize()
    return jsonify(people), 200


# -----------------------------------------Get Todos los Planetas-----------------------------------------------------------------------------

@app.route('/planets', methods=['GET'])
def get_planets():

    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    # Otra alternativa para serializar, cuando se consulta al modelo no se pude transformar directamente a un json, por eso se serializa
    # all_people = [person.serialize() for person in Person.query.all()]

    if all_planets is None:
        response_body = {
            "msg": "Not planets found"
        }
        return jsonify(response_body), 404

    return jsonify(all_planets), 200


# -----------------------------------------Get Planet por id-------------------------------------------------------------------------------------

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):

    planet = Planet.query.get(planet_id)

    if planet is None:
        response_body = {
            "msg": "Not planet with id: {" + str(planet_id) + "} found"
        }
        return jsonify(response_body), 404

    planet = planet.serialize()
    return jsonify(planet), 200


# -----------------------------------------Get Todos los Usuarios-----------------------------------------------------------------------------

@app.route('/users', methods=['GET'])
def get_users():

    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
  
    if all_users is None:
        response_body = {
            "msg": "Not users found"
        }
        return jsonify(response_body), 404

    return jsonify(all_users), 200


# -----------------------------------------Get Todos los Favoritos de un usuari0-----------------------------------------------------------------------------

@app.route('/users/favorites', methods=['GET'])
def get_users_favorites():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# -----------------------------------------Agrega un planet favorito al usuario actual con el id: planet_id, tambien elimina-----------------------------------------------------------------------------

@app.route('/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def manage_favorite_planet():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# -----------------------------------------Agrega un people favorito al usuario actual con el id: people_id, tambien elimina-----------------------------------------------------------------------------

@app.route('/favorite/people/<int:people_id>', methods=['POST', 'DELETE'])
def manage_favorite_people():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# --------------------------------------------------------------------------------------------------------------------------------------------------
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
