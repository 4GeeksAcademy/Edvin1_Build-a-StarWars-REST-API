from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

## cuando se modifica la tabla -> pipenv run migrate -> pipenv run upgrade/downgrade

user_group = db.Table('user_group',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id', primary_key=True)),
                      db.Column('group.id', db.Integer, db.ForeignKey('groups.id', primary_key=True))
                      )

class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(150))
    country = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    #relation posts
    posts = db.relationship('Posts', back_populates='user', lazy=True)

    #relation muchos a muchos
    groups = db.relationship('Groups', secondary=user_group, back_populates='users')

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
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='posts')



    def __repr__(self):
        return '<Posts %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content" : self.content,
            "user_id" : self.user_id
        }
    
class Groups(db.Model):
    __tablename__= 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_group, back_populates='groups')


class People(db.Model):
    __tablename__= 'people'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)


    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
    

