from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

## cuando se modifica la tabla -> pipenv run migrate -> pipenv run upgrade/downgrade

class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(150))
    country = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    posts = db.relationship('Posts', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "city" : self.city,
            "is_active" : self.is_active
            # do not serialize the password, its a security breach
        }
    
class Posts(db.Model):
    __tablename__= 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True, nullable=False)
    content = db.Column(db.String(250), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



    def __repr__(self):
        return '<Posts %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content" : self.content,
            "user_id" : self.user_id
        }
    
class Group