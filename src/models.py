from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(50))
    orbit = db.Column(db.String(50))
    population = db.Column(db.String(50))
    description = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='planets')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "orbit": self.orbit,
            "population": self.population,
            "description": self.description
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(50))
    eyes = db.Column(db.String(50))
    height = db.Column(db.String(50))
    description = db.Column(db.String(250))
    favorites = db.relationship('Favorites', backref='people')


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "sex": self.sex,
            "eyes": self.eyes,
            "height": self.height,
            "description": self.description
        }


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'),nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'),nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "people_id": self.people_id,
            "user_id": self.user_id
        }