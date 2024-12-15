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
from models import db, User, Posts
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

@app.route('/users', methods=['GET'])
def handle_all():
    users = User.query.all()
    users = [user.serialize() for user in users]
    return jsonify(users), 200

@app.route('/posts', methods=['GET'])
def handle_get_posts():
    posts = Posts.query.all()
    posts = [post.serialize() for post in posts]
    return jsonify(posts), 200


@app.route('/user/<int:id>', methods=['GET'])
def handle_one(id):
    user = User.query.get(id)
    respObj = {
        "success" : True,
        "data" : user.serialize()
    }
    return jsonify(respObj), 200


@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(
        email = data["email"],
        password = data["password"],
        city = data["city"],
        country = data["country"],
        is_active = data["is_active"]
        )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
