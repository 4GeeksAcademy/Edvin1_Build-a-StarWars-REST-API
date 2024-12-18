from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

## cuando se modifica la tabla -> pipenv run migrate -> pipenv run upgrade/downgrade

class Users(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    favourites = db.relationship('Favourites', backref='users', lazy=True)


    def __repr__(self):
        return '<Users %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active" : self.is_active
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__= 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    species = db.Column(db.String(50), nullable=True)    

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "species": self.species
        }
    
class Planets(db.Model):
    __tablename__= 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    population = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return '<Planets %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate
        }

class Favourites(db.Model):
    __tablename__='favourites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

    def __repr__(self):
        return '<Favourites UserID %r>' % self.user_id
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }


