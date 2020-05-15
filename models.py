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
    release_date = db.Column(db.Date(), nullable=False)
    actors = db.relationship(
        'Actor', secondary=association_table, backref=db.backref('movies', cascade="all, delete", lazy='joined'))

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def add_actors(self, actor):
        if actor not in self.actors:
            self.actors.append(actor)
        self.update()

    def delete_actor(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)

    def get_actors(self):
        actors_list = []
        for actor in self.actors:
            actors_list.append(actor.format())
        return({
            'actors': actors_list
        })

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):

        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

    def __repr__(self):
        return json.dumps(self.format())


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def add_movie(self, movie):
        if movie not in self.movies:
            self.movies.append(movie)

    def delete_movie(self, movie):
        if movie in self.movies:
            self.movies.remove(movie)

    def get_movies(self):
        movies_list = []
        for movie in self.movies:
            movies_list.append(movie.format())
        return({
            'movies': movies_list
        })

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
        }

    def __repr__(self):
        return json.dumps(self.format())
