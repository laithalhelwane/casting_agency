import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, association_table, db


def is_none(*request_body):
    for attribute in request_body:
        if attribute is None:
            return True
    return False


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        # Set Access-Control-Allow Headers
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Method',
                             'GET, POST, DELETE, PATCH')
        return response
    # ----Actors-----

    @app.route('/actors', methods=['GET'])
    def get_actors():
        try:
            actors = Actor.query.all()
            data = []

            for actor in actors:
                data.append({"actor's_informaion": actor.format(),
                             "actor's_movies": actor.get_movies()})

            return jsonify({
                'success': True,
                'actors': data
            })

        except Exception:
            abort(422)

    @app.route('/actors/<int:id>', methods=['GET'])
    def get_actor(id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if is_none(actor):
            abort(404)
        return jsonify({
            'success': True,
            "actor's_informaion": actor.format(),
            "actor's_movies": actor.get_movies()
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actor(id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if is_none(actor):
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'deleted': id
            })
        except Exception:
            abort(422)

    @app.route('/actors', methods=['POST'])
    def add_actor():
        body = request.get_json()
        if is_none(body.get('name'), body.get('age'), body.get('gender')):
            abort(400)
        try:
            new_actor = Actor(name=body.get('name'), age=body.get(
                'age'), gender=body.get('gender'))
            new_actor.insert()
            return jsonify({
                'success': True,
                'actor': new_actor.format()
            })
        except Exception:
            abort(422)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    def edit_actor_data(id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)
        try:
            body = request.get_json()
            if body.get('name') is not None:
                actor.name = body.get('name')
            if body.get('age') is not None:
                actor.age = body.get('age')
            if body.get('gender') is not None:
                actor.gender = body.get('gender')
            actor.update()
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception:
            abort(422)

    # ----- Movies -----

    @app.route('/movies', methods=['GET'])
    def get_movies():
        try:
            movies = Movie.query.all()
            data = []

            for movie in movies:
                data.append(movie.format())

            return jsonify({
                'success': True,
                'movies': data
            })

        except Exception:
            abort(422)

    @app.route('/movies/<int:id>', methods=['GET'])
    def get_movie(id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if is_none(movie):
            abort(404)
        return jsonify({
            'success': True,
            'movie_informations': movie.format(),
            "movie's_actors": movie.get_actors()
        })

    @app.route('/movies/<int:id>', methods=['DELETE'])
    def delete_movie(id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if is_none(movie):
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'deleted': id
            })
        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    def add_movie():
        body = request.get_json()
        if is_none(body.get('title'), body.get('release_date')):
            abort(400)  # bad request
        try:
            new_movie = Movie(title=body['title'],
                              release_date=body['release_date'])
            new_movie.insert()

            return jsonify({
                'success': True,
                'movie': new_movie.format(),
                "movie's_actors": new_movie.get_actors()
            })
        except Exception:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    def edit_movie_data(id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if is_none(movie):
            abort(404)
        try:
            body = request.get_json()
            if not is_none(body.get('title')):
                movie.title = body.get('title')
            if not is_none(body.get('release_date')):
                movie.release_date = body.get('release_date')
            movie.update()
            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except Exception:
            abort(422)

    @app.route('/assign', methods=['POST'])
    def assign_actor():
        body = request.get_json()
        if is_none(body.get('actor_id'), body.get('movie_id')):
            abort(400)
        actor_id = body.get('actor_id')
        movie_id = body.get('movie_id')
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if is_none(actor, movie):
            abort(404)
        try:
            movie.add_actor(actor)
            return jsonify({
                'success': True,
                "movie's_actor": movie.get_actors()
            })
        except Exception:
            abort(422)
    @app.route('/assign', methods=['DELETE'])
    def unassign_actor():
        body = request.get_json()
        if is_none(body.get('actor_id'), body.get('movie_id')):
            abort(400)
        actor_id = body.get('actor_id')
        movie_id = body.get('movie_id')
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if is_none(actor, movie):
            abort(404)
        try:
            movie.delete_actor(actor)
            return jsonify({
                'success': True,
                "movie's_actor": movie.get_actors()
            })
        except Exception:
            abort(422)
    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
