import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db, Actor, Movie, association_table

producer_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeH\
d5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2Z\
zbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZ\
TY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXB\
zdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk5M\
TE1MzksImV4cCI6MTU4OTk5NzkzOSwiYXpwIjoibnZFWW9oRWR\
kcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsI\
nBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSI\
sImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6Y\
WN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDp\
tb3ZpZXMiXX0.NZlTPglsb6rmYE3V386Cgw8p9drR55H8OcoAT\
06ydNmClYR8sFki1iDcXHceDx9AV7o0kZtG-wiq9LVnLpNTOUG\
VcP5caba2DuqRl5QsvNuxlatioerbIIHgT66ZBRf-2cPqOuk1B\
4EtwJJtpw_CixSOSVc6wncPCWu4WrAMY8O0mL0ECGbNi-B6OKu\
EmwVF2r7LYBfRo3Qnl1OuUg6Q_J6GMT8LB6dC3jcStCg0YoJT-\
8oTfA1KDxogmnTqiVl6spMa6WzmD9RKUuHY5EKu0sVVoOqKTSM\
l0kItWgmJflaz4oYga7D97R-PSp1NitLoW3z15GIVRVmoa1-QZ\
rDncg'
assistant_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeH\
d5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2Z\
zbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZkN\
TdjMWIzNWM0MGJlNDQyYTVjYyIsImF1ZCI6Imh0dHA6Ly9jYXB\
zdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk5M\
TE4ODcsImV4cCI6MTU4OTk5ODI4NywiYXpwIjoibnZFWW9oRWR\
kcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsI\
nBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWV\
zIl19.c5jfVfHuocB5_TbNToHJtHhpZuRRQU8I-PB56dFAHin-\
usv4zX6M4le7kOaP_wlvn_g9798D6oX2YnUZp_Pt5x4zAfBBkd\
p3eccXTVi0IpOgbSLwqKI_HLH1chkZtTWOssZ_XUulrlX-BDFY\
CEEcjK87CL41623rYyxhoVZSHa_bf9FGNIushG73Q5aqMYlhLO\
sVILnaYnvErWibq7xT1RGbab1PtkWIs5JA-ogcf8v7OTbJffoP\
xxzOxF_kAmRGi0KeROuqvEmBoitPyfp0gC5TomFdnWaadrVdyi\
evkOhajPbM3B97_J_IvaoPgqmEVS_VfvExvQ8G7JbvIgl9qQ'
director_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeH\
d5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2Z\
zbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZkN\
mU4YmY5Mjk4MGJkMGVhZGJhNSIsImF1ZCI6Imh0dHA6Ly9jYXB\
zdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk5M\
TIwMDgsImV4cCI6MTU4OTk5ODQwOCwiYXpwIjoibnZFWW9oRWR\
kcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsI\
nBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImRlbGV0ZTphY3R\
vciIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjd\
G9ycyIsImdldDptb3ZpZXMiXX0.noYBh8lwPPdLp9DeNmxePwS\
VW-04Wh2P66GuhvxnNCn4n29TSyDmtLmoKeFnZequwVKRTpx1K\
OfrSSZeBIbD0OacMkGL3FiXqrgz9Pf4L2DbxGFeifnrgsWCbh_\
sCjPFaQMiq0sYAD5v-FPPZHZSi9tRE9hfvgOrYtXbJdVN1llO-\
AqivfgYyww43rhni1bA7wRuzvm5qctbFHsanx4WoPP1glu8AqY\
fDZ1shKpKRgwbraos3T1_ZREjomH8H8bDqeNckGvfAUHUiJlfY\
xkz7g3GAzjwSEdmiP5CQNxoTsDR_JWyQQFecJ4jefr0aAV_WpL\
pzJXJeY-C8muhfMLW4A'


class CapstoneTestCase(unittest.TestCase):
    ''' This Class represents the app test case '''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL_TEST']
        setup_db(self.app, self.database_path)

        # sample actor for use in tests
        self.new_actor = {
            'name': 'actor test',
            'age': 13,
            'gender': 'male'
        }
        # sample movie for use in tests
        self.new_movie = {
            'title': 'movie test',
            'release_date': '2020-10-10'
        }

        # sample assign for use in tests
        self.new_assign = {
            'artist_id': 1,
            'movie_id': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # Create all tables
            db.create_all()

    # Drop the database after every test

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # -- Successful test for every Endpoint using jwt with producer premissions

    # test get the list of actors from the database

    def test_get_actors(self):
        # Add new Actor to the database
        actor = Actor(
            name=self.new_actor['name'],
            age=self.new_actor['age'],
            gender=self.new_actor['gender'])
        actor.insert()

        # Send the request and load response data
        response = self.client().get(
            '/actors', headers={'Authorization': f'Bearer {producer_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('success'), True)

        # Check if data included
        self.assertIsNotNone(data.get('actors'))
        self.assertEqual(len(data.get('actors')), 1)

    # test add new actor to the database

    def test_add_actor(self):

        # create new actor and load response data
        response = self.client().post(
            '/actors',
            headers={'Authorization': f'Bearer {producer_jwt}'},
            json=self.new_actor)
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('success'), True)

        # see if the Actor has been created
        actor = Actor.query.filter(
            Actor.id == data['actor']['id']).one_or_none()

        # check that question is not None
        self.assertIsNotNone(actor)

    # Test get user information from database by id
    def test_get_actor_by_id(self):
        # Add new Actor to the database
        actor = Actor(
            name=self.new_actor['name'],
            age=self.new_actor['age'],
            gender=self.new_actor['gender'])
        actor.insert()

        # Send the request and load response data
        response = self.client().get(
            'actors/{}'.format(actor.id),
            headers={'Authorization': f'Bearer {producer_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("success"), True)

        # check if actor information are included and correct
        self.assertIsNotNone(data.get("actor's_information"))
        self.assertEqual(data.get("actor's_information").get('id'), actor.id)
        self.assertEqual(
            data.get("actor's_information").get('name'), actor.name)
        self.assertEqual(data.get("actor's_information").get('age'), actor.age)
        self.assertEqual(data.get("actor's_information").get(
            'gender'), actor.gender)

    # Test Delete actor form database by id

    def test_delete_actor_by_id(self):
        # Add new Actor to the database
        actor = Actor(
            name=self.new_actor['name'],
            age=self.new_actor['age'],
            gender=self.new_actor['gender'])
        actor.insert()
        actor_id = actor.id

        # Send the request and load response data
        response = self.client().delete(
            'actors/{}'.format(actor.id),
            headers={'Authorization': f'Bearer {producer_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("success"), True)

        # Check if the actor is deleted from the database
        self.assertEqual(data.get('deleted'), actor_id)
        self.assertIsNone(Actor.query.filter(
            Actor.id == actor_id).one_or_none())

    # Test edit actor information form database by id

    def test_edit_actor_by_id(self):
        # Add new Actor to the database
        actor = Actor(
            name=self.new_actor['name'],
            age=self.new_actor['age'],
            gender=self.new_actor['gender'])
        actor.insert()

        # Send the request and load response data
        response = self.client().patch(
            'actors/{}'.format(actor.id),
            headers={'Authorization': f'Bearer {producer_jwt}'},
            json={'name': 'test PATCH'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("success"), True)

        # Check if the actor is edited
        self.assertIsNotNone(data.get('actor'))
        self.assertEqual(data.get('actor').get('name'), 'test PATCH')
        self.assertEqual(data.get('actor').get('age'), actor.age)
        self.assertEqual(data.get('actor').get('gender'), actor.gender)

    # test get the list of movies from the database

    def test_get_movies(self):
        # Add new Movie to the database
        movie = Movie(
            title=self.new_movie['title'],
            release_date=self.new_movie['release_date'])
        movie.insert()

        # Send the request and load response data
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {producer_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('success'), True)

        # Check if data included
        self.assertIsNotNone(data.get('movies'))
        self.assertEqual(len(data.get('movies')), 1)

    # test add new Movie to the database

    def test_add_movie(self):

        # create new movie and load response data
        response = self.client().post(
            '/movies',
            headers={'Authorization': f'Bearer {producer_jwt}'},
            json=self.new_movie)
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('success'), True)

        # see if the Movie has been created
        movie = Movie.query.filter(
            Movie.id == data['movie']['id']).one_or_none()

        # check that question is not None
        self.assertIsNotNone(movie)

    # Test get Movie information from database by id
    def test_get_movie_by_id(self):
        # Add new Movie to the database
        movie = Movie(
            title=self.new_movie['title'],
            release_date=self.new_movie['release_date'])
        movie.insert()

        # Send the request and load response data
        response = self.client().get(
            'movies/{}'.format(movie.id),
            headers={'Authorization': f'Bearer {producer_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("success"), True)

        # check if Movie information are included and correct
        self.assertIsNotNone(data.get("movie_information"))
        self.assertEqual(data.get("movie_information").get('id'), movie.id)
        self.assertEqual(
            data.get("movie_information").get('title'), movie.title)

    # Test Delete movie form database by id

    def test_delete_movie_by_id(self):
        # Add new movie to the database
        movie = Movie(
            title=self.new_movie['title'],
            release_date=self.new_movie['release_date'])
        movie.insert()
        movie_id = movie.id

        # Send the request and load response data
        response = self.client().delete(
            'movies/{}'.format(movie.id),
            headers={'Authorization': f'Bearer {producer_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("success"), True)

        # Check if the actor is deleted from the database
        self.assertEqual(data.get('deleted'), movie_id)
        self.assertIsNone(Movie.query.filter(
            Movie.id == movie_id).one_or_none())

    # Test edit movie information form database by id

    def test_edit_movie_by_id(self):
        # Add new Movie to the database
        movie = Movie(
            title=self.new_movie['title'],
            release_date=self.new_movie['release_date'])
        movie.insert()

        # Send the request and load response data
        response = self.client().patch(
            'movies/{}'.format(movie.id),
            headers={'Authorization': f'Bearer {producer_jwt}'},
            json={'title': 'test PATCH'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("success"), True)

        # Check if the movie is edited
        self.assertIsNotNone(data.get('movie'))
        self.assertEqual(data.get('movie').get('title'), 'test PATCH')

    # Test assing relationship between movie and actor
    def test_assign(self):
        # Add new Actor to the database
        actor = Actor(
            name=self.new_actor['name'],
            age=self.new_actor['age'],
            gender=self.new_actor['gender'])
        actor.insert()

        # Add new Movie to the database
        movie = Movie(
            title=self.new_movie['title'],
            release_date=self.new_movie['release_date'])
        movie.insert()

        # Send the request and load response data
        response = self.client().post(
            '/assign',
            headers={'Authorization': f'Bearer {producer_jwt}'},
            json={
                'actor_id': actor.id,
                'movie_id': movie.id
            })

        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("success"), True)

        self.assertIsNotNone(data.get("movie's_actor"))
        self.assertIn(actor, movie.actors)
        self.assertIn(movie, actor.movies)

        # Test delete relationship between movie and actor
    def test_unassign(self):
        # Add new Actor to the database
        actor = Actor(
            name=self.new_actor['name'],
            age=self.new_actor['age'],
            gender=self.new_actor['gender'])
        actor.insert()

        # Add new Movie to the database
        movie = Movie(
            title=self.new_movie['title'],
            release_date=self.new_movie['release_date'])
        movie.insert()

        # Send the request and load response data
        response = self.client().delete(
            '/assign',
            headers={'Authorization': f'Bearer {producer_jwt}'},
            json={
                'actor_id': actor.id,
                'movie_id': movie.id
            })

        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get("success"), True)

        self.assertIsNotNone(data.get("movie's_actor"))
        self.assertNotIn(actor, movie.actors)

    # Unsuccessful test for every Endpoint using jwt with producer premissions

    # test send bad request (with out actor information)
    def test_401_add_actor(self):

        # create new actor and load response data
        response = self.client().post(
            '/actors',
            headers={'Authorization': f'Bearer {producer_jwt}'},
            json={})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data.get('success'), False)

    # test get actor not in the database
    def test_404_get_actor_by_id(self):

        # Send the request and load response data
        response = self.client().get(
            'actors/{}'.format(1),
            headers={'Authorization': f'Bearer {producer_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("success"), False)

    # test delete actor not in the database
    def test_404_delete_actor_by_id(self):

        # Send the request and load response data
        response = self.client().get(
            'actors/{}'.format(1),
            headers={'Authorization': f'Bearer {producer_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("success"), False)

    # test send bad request (with out movie information)
    def test_401_add_movie(self):

        # create new actor and load response data
        response = self.client().post(
            '/movies',
            headers={'Authorization': f'Bearer {producer_jwt}'},
            json={})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data.get('success'), False)

    # test get movie not in the database
    def test_404_get_movie_by_id(self):

        # Send the request and load response data
        response = self.client().get(
            'movies/{}'.format(1),
            headers={'Authorization': f'Bearer {producer_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("success"), False)

    # test delete movie not in the database
    def test_404_delete_movie_by_id(self):

        # Send the request and load response data
        response = self.client().get(
            'movies/{}'.format(1),
            headers={'Authorization': f'Bearer {producer_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data.get("success"), False)

    # --- Add RBAC tests ---

    # test delete movie using jwt with director premissions
    def test_401_delete_movie(self):
        movie = Movie(
            title=self.new_movie['title'],
            release_date=self.new_movie['release_date'])
        movie.insert()

        # Send the request and load response data
        response = self.client().delete(
            'movies/{}'.format(movie.id),
            headers={'Authorization': f'Bearer {director_jwt}'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data.get("success"), False)

    # test edit movie using jwt with assistant premissions

    def test_401_edit_movie(self):
        # Add new Movie to the database
        movie = Movie(
            title=self.new_movie['title'],
            release_date=self.new_movie['release_date'])
        movie.insert()

        # Send the request and load response data
        response = self.client().patch(
            'movies/{}'.format(movie.id),
            headers={'Authorization': f'Bearer {assistant_jwt}'},
            json={'name': 'test PATCH'})
        data = json.loads(response.data)

        # check status code and success message
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data.get("success"), False)


if __name__ == "__main__":
    unittest.main()
