import os
from sqlalchemy import Column, String, Integer, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import json
'''
    Setup database path
'''
database_path = os.environ['DATABASE_URL']


db = SQLAlchemy()

'''
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
    Association Table for actor and movie (Many to Many) relationship
'''
association_table = db.Table('association',
                             db.Column('movie_id', db.Integer,
                                       db.ForeignKey('movies.id')),
                             db.Column('actor_id', db.Integer,
                                       db.ForeignKey('actors.id'))
                             )


class Movie(db.Model):
    # Table name in the database
    __tablename__ = 'movies'
    # Autoincrementing, unique primary ke
    id = db.Column(db.Integer, primary_key=True)

    # String Title
    title = db.Column(db.String(250), nullable=False)

    # release date
    release_date = db.Column(db.Date(), nullable=False)

    # Create relationship between movie and actor
    actors = db.relationship(
        'Actor', secondary=association_table, backref=db.backref('movies', cascade="all, delete", lazy='joined'))

    # Movie Constructor
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    # Insert new Movie into database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Add new relationship between movie and actor
    def add_actor(self, actor):
        if actor not in self.actors:
            self.actors.append(actor)
        self.update()

    # Delete the relationship between movie and actor
    def delete_actor(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)
        self.update()

    # Get list movie's actors
    def get_actors(self):
        actors_list = []

        for actor in self.actors:
            actors_list.append(actor.format())

        return({
            'actors': actors_list
        })
    # Update Movie

    def update(self):
        db.session.commit()

    # Delete the movie from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # Return Movie information in JSON format 
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

    def __repr__(self):
        return json.dumps(self.format())


class Actor(db.Model):
    # Table Name in the Database
    __tablename__ = 'actors'

    # Autoincrementing, unique primary ke
    id = db.Column(db.Integer, primary_key=True)

    # Name Strign
    name = db.Column(db.String(250), nullable=False)

    # Age Integer
    age = db.Column(db.Integer(), nullable=False)

    # Gender String
    gender = db.Column(db.String(), nullable=False)

    # Actor Constructor
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    # Add new relationship between movie and actor
    def add_movie(self, movie):
        if movie not in self.movies:
            self.movies.append(movie)
        self.update()
    # Delete the relationship between movie and actor
    def delete_movie(self, movie):
        if movie in self.movies:
            self.movies.remove(movie)
        self.update()

    # Get list actor's movies
    def get_movies(self):
        movies_list = []

        for movie in self.movies:
            movies_list.append(movie.format())

        return({
            'movies': movies_list
        })

    # Insert the Actor in the database
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    # Update Actor
    def update(self):
        db.session.commit()

    # Delete Actor from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # Return Actor information in JSON format 
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

    def __repr__(self):
        return json.dumps(self.format())
