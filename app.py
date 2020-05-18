import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, association_table, db
from auth.auth import AuthError, requires_auth

'''
    return True if one of it's arguments is None
'''


def is_none(*args):
    for arg in args:
        if arg is None:
            return True
    return False


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    '''
    Set Access-Control-Allow Headers
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Method',
                             'GET, POST, DELETE, PATCH')
        return response


# ---- Actor Endpoints ----

    '''
        route handler to get list of actors
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(token):
        try:
            actors = Actor.query.all()  # Get all actors in the database
            data = []

            for actor in actors:
                # format actor information
                data.append({
                    "actor's_information": actor.format(),
                    "actor's_movies": actor.get_movies()
                })

            return jsonify({
                'success': True,
                'actors': data
            })

        except Exception:
            abort(422)  # unprocessable

    '''
        route handler to get actor by id
    '''

    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(token, id=id):
        # Retrive the actor from the database
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if is_none(actor):  # Check if the actor is not exist
            abort(404)  # not found

        return jsonify({
            'success': True,
            "actor's_information": actor.format(),
            "actor's_movies": actor.get_movies()
        })
    '''
        route handler to delete actor by id
    '''
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(token, id=id):
        # Retrive the actor from the database
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if is_none(actor):  # Check if the actor is not exist
            abort(404)  # not found

        try:
            actor.delete()
            return jsonify({
                'success': True,
                'deleted': id
            })

        except Exception:
            abort(422)  # unprocessable
    '''
        route handler to add new actor
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actor')
    def add_actor(token):
        body = request.get_json()

        '''
            Check if all information are included in the request
        '''
        if is_none(
                body.get('name'),
                body.get('age'),
                body.get('gender')):
                abort(401)  # bad request

        try:
            '''
                Create new Actor
            '''
            new_actor = Actor(
                name=body.get('name'),
                age=body.get('age'),
                gender=body.get('gender'))

            new_actor.insert()

            return jsonify({
                'success': True,
                'actor': new_actor.format()
            })

        except Exception:
            abort(422)  # unprocessable
    '''
        route handler to edit actor information
    '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('edit:actor')
    def edit_actor_data(token, id=id):
        # Retrive the actor from the database
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if is_none(actor):  # Check if the actor is not exist
            abort(404)  # not found

        try:

            body = request.get_json()
            '''
                Check what information are included in the request body,
                and edit the actor based on it
            '''
            if not is_none(body.get('name')):
                actor.name = body.get('name')

            if not is_none(body.get('age')):
                actor.age = body.get('age')

            if not is_none(body.get('gender')):
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except Exception:
            abort(422)  # unprocessable

    # ----- Movies Endpoints -----

    '''
        route handler to get list of movies
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(token):
        try:
            movies = Movie.query.all()  # Get all movies in the database
            data = []

            for movie in movies:
                # format movie information
                data.append({
                    "movie's_information": movie.format(),
                    "movie's_movies": movie.get_actors()
                })

            return jsonify({
                'success': True,
                'movies': data
            })

        except Exception:
            abort(422)  # unprocessable
    '''
        route handler to get movie by id
    '''
    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(token, id=id):
        # Retrive the movie from the database
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if is_none(movie):  # Check if the movie is not exist
            abort(404)  # not found

        return jsonify({
            'success': True,
            'movie_information': movie.format(),
            "movie's_actors": movie.get_actors()
        })

    '''
        route handler to delete movie by id
    '''
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(token, id=id):
        # Retrive the movie from the database
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if is_none(movie):  # Check if the movie is not exist
            abort(404)  # not found

        try:

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': id
            })

        except Exception:
            abort(422)  # unprocessable

    '''
        route handler to add new movie
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movie')
    def add_movie(token):
        body = request.get_json()

        '''
            Check if all information are included in the request
        '''

        if is_none(
                body.get('title'),
                body.get('release_date')):
                abort(401)  # bad request
        try:
            '''
                Create new Movie
            '''
            new_movie = Movie(
                title=body['title'],
                release_date=body['release_date']
            )

            new_movie.insert()

            return jsonify({
                'success': True,
                'movie': new_movie.format(),
                "movie's_actors": new_movie.get_actors()
            })

        except Exception:
            abort(422)  # unprocessable

    '''
        route handler to edit movie information
    '''

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('edit:movie')
    def edit_movie_data(token, id=id):
        # Retrive the movie from the database
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if is_none(movie):  # Check if the movie is not exist
            abort(404)  # not found
        try:

            body = request.get_json()
            '''
                Check what information are included in the request body,
                and edit the movie based on it
            '''
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
            abort(422)  # unprocessable

    # ---- Assign ----
    '''
        Assign Endpoint add relationship between actor and movie
    '''
    @app.route('/assign', methods=['POST'])
    @requires_auth('edit:movie')
    def assign_actor(token):
        body = request.get_json()

        '''
            Check if all information are included in the request
        '''

        if is_none(
            body.get('actor_id'),
            body.get('movie_id')
        ):
            abort(401)  # bad request

        actor_id = body.get('actor_id')
        movie_id = body.get('movie_id')

        '''
        Retrive the Movie and The Actor from the database
        '''

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if is_none(actor, movie):  # Check if any of them is not exist
            abort(404)  # not found

        try:

            movie.add_actor(actor)

            return jsonify({
                'success': True,
                "movie's_actor": movie.get_actors()
            })

        except Exception:
            abort(422)  # unprocessable

    '''
        Assign:Delete Endpoint remove relationship between actor and movie
    '''

    @app.route('/assign', methods=['DELETE'])
    @requires_auth('edit:movie')
    def unassign_actor(token):
        body = request.get_json()

        '''
            Check if all information are included in the request
        '''

        if is_none(
            body.get('actor_id'),
            body.get('movie_id')
        ):
            abort(401)  # bad request

        actor_id = body.get('actor_id')
        movie_id = body.get('movie_id')

        '''
        Retrive the Movie and The Actor from the database
        '''

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if is_none(actor, movie):  # Check if any of them is not exist
            abort(404)

        try:

            movie.delete_actor(actor)

            return jsonify({
                'success': True,
                "movie's_actor": movie.get_actors()
            })

        except Exception:
            abort(422)  # unprocessable

    # ---- Error Handlers ----

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found',
        }), 404

    @app.errorhandler(401)
    def notfound(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized',
        }), 401

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request',
        }), 400

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': error.error['description'],
        }), 401

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
