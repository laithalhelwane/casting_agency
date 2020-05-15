import os
from sqlalchemy import Column, String, Integer, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import json
'''
    Setup database path
'''
# database_path = os.environ['DATABASE_URL']
database_path = 'postgresql://postgres:admin@localhost:5432/app'

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


association_table = db.Table('association',
                             db.Column('movie_id', db.Integer,
                                       db.ForeignKey('movies.id')),
                             db.Column('actor_id', db.Integer,
                                       db.ForeignKey('actors.id'))
                             )


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    release_date = db.Column(db.DateTime(), nullable=False)
    actors = db.relationship(
        'Actor', secondary=association_table, backref=db.backref('movies', cascade="all, delete-orphan", lazy='joined'))

    def __init__(self, title, release_date):
        this.title = title
        this.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def add_actors(self, actor_list):
        for actor in actor_list:
            self.actors.append(actor)

    def delete_actor(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'title': self.title,
            'release_date': self.release_date,
            'actors': self.actors
        }

    def __repr__(self):
        return json.dumps(self.format())


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer())
    gender = db.Column(db.String())

    def __init__(self, name, age, gender):
        this.name = name
        this.age = age
        this.gender = gender

    def add_movies(self, movies_list):
        for movie in movies_list:
            self.actors.append(movie)

    def delete_movie(self, movie):
        if movie in self.movies:
            self.movies.remove(movie)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'mobies': self.movies
        }

    def __repr__(self):
        return json.dumps(self.format())
