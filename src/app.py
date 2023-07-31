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
from models import db, User, Planets, People, Favorites
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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

        #the user---------

@app.route('/user/<int:user_id>', methods=['GET'])
def find_user(user_id):
    user_id = User.query.get(user_id)
    if not user_id:
        return jsonify(message='user not found'), 404
    return jsonify(user_id)

@app.route('/user', methods=['GET'])
def Get_users():
    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200


@app.route('/user', methods=['POST'])
def create_user():
    user = User()
    data = request.get_json()
    user.username = data.get('username')
    user.email = data.get('email')
    user.password = data.get('password')
    user.phone_number = data.get('phone_number')

    if not user.username or not user.email or not user.password or not user.phone_number:
        return jsonify(message='Missing required fields'), 400

    return jsonify(user.serialize()), 201


@app.route('/user/favorites', methods=['GET'])
def user_faves():
    favorites = Favorites.query.all()
    all_favorites = list(map(lambda x: x.serialize(), favorites))
    return jsonify(all_favorites), 200


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User(email = request.get_json()['user_email'],password = request.get_json()['user_password'], id= user_id)
    if user is None:
        return jsonify('User not found')
    db.session.delete(user)
    return jsonify('User deleted')




        #the planets-----------

@app.route('/planets', methods=['GET'])
def planetsLink():
    planets = Planets.query.all()
    planets_arrays = list(map(lambda item: item.serialize(),planets))
    return jsonify(planets_arrays), 200

@app.route('/planets/<int:planets_id>', methods=['GET'])
def planetsID(planets_id):
    planet_id = Planets.query.get(planets_id)
    return jsonify(planet_id), 200

@app.route('/favorites/planets/<int:planets_id>', methods=['POST'])
def fave_planets(planets_id):
    favorite_planets = Favorites(user_id = request.get_json()['user_id'], planets_id=planets_id)
    db.session.add(favorite_planets)
    db.session.commit()
    return jsonify('favorite planet added')



        #the people--------

@app.route('/people', methods=['GET'])
def peopleLink():
    people = People.query.all()
    people_array = list(map(lambda item: item.serialized(), people))
    return jsonify(people_array), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def peopleID(people_id):
    person: People.query.get(people_id)
    return jsonify(person), 200

@app.route('/favorites/people/<int:people_id>', methods=['POST'])
def fave_people(people_id):
    favorite_people = Favorites(user_id = request.get_json()['user_id'], people_id=people_id)
    db.session.add(favorite_people)
    db.session.commit()
    return jsonify('favorite person added')


        #deleting favorite planets/people

@app.route('/favorites/planets/<int:planets_id>', methods=['DELETE'])
def delete_favorite_planet(planets_id):
    favorite_planets = Favorites.query.filter_by(user_id = request.get_json()['user_id'], planets_id=planets_id).first()
    if favorite_planets is None:
        return jsonify('Planet not found')
    db.session.delete(favorite_planets)
    return jsonify('favorite planet deleted')


@app.route('/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite_people = Favorites.query.filter_by(user_id = request.get_json()['user_id'], people_id=people_id).first()
    if favorite_people is None:
        return jsonify('People not found')
    db.session.delete(favorite_people)
    return jsonify('favorite people deleted')

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
