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
from models import db, Users, Planets, People, Favourites
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

#####
# 1. people endpoints
@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    serialized_people = [person.serialize() for person in people]
    return jsonify(serialized_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person():
    person = People.query.get(people_id)               ### error aqui??
    if not person:
        return jsonify({"msg": "Person not found"}), 404   
    return jsonify(person.serialize()), 200

# 2. Planets endpoints

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planets.query.all()                                                   # poner nombre de clase o tabla???
    serialized_planets = [planet.serialize() for planet in planets]
    return jsonify(serialized_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet():
    planet = Planets.query.all()
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# 3. User endpoints

@app.route('/users', methods=['GET'])
def get_all_users():
    users = Users.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify(serialized_users), 200

@app.route('/users/favourites', methods=['GET'])
def get_user_favourites():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"msg": "User ID is required"}), 400
    
    favourites = Favourites.query.filter_by(user_id=user_id).all()
    serialized_favourites = [favourite.serialize() for favourite in favourites]
    return jsonify(serialized_favourites), 200

# 4. Add favourites

@app.route('/favourite/planet/<int:planet_id>', methods=['POST']) 
def add_favourite_planet(planet_id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"User ID is required"}), 400
    
    new_favourite = Favourites(user_id = user_id, planet_id = planet_id)       
    db.session.add.new(new_favourite)
    db.session.commit()
    return jsonify({"msg": "Favourite planet added succesfully"}), 201

@app.route('/favourite/people/<int:people_id>', methods=['POST'])
def add_favourite_people(people_id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"msg": "User ID is required"}), 400
    
    new_favourite = Favourites(user_id = user_id, people_id = people_id)
    db.session.add(new_favourite)
    db.session.commit()
    return jsonify({"Favourite person added succesfully"}), 201

# 5. Delete favorourites

@app.route('/favourite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favourite_planet(planet_id):
    user_id = request.json.get("user_id")
    favourite = Favourites.query.filter_by(user_id = user_id, planet_id = planet_id). first()

    if not favourite:
        return jsonify({"Favourite planet not found"}), 404
    
    db.session.delete(favourite)
    db.session.commit()
    return jsonify({"msg": "favourite planet deleted succesfully"}), 200

@app.route('/favourite/people/<int:people_id>', methods=['DELETE'])
def delete_favourite_people(people_id):
    user_id= request.json.get("user_id")
    favourite = Favourites.query.all.filter_by(user_id = user_id, planet_id = planet_id).first()

    if not favourite:
        return jsonify({"msg": "Favourite person not found"}), 404
    
    db.session.delete(favourite)
    db.session.commit()
    return jsonify({"msg": "Favorite person deleted successfully"}), 200



###

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
