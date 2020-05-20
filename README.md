# Casting Agency Backend

## Introduction
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/. (main directory)` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the postgres database

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTs.

### Running the server

From within the `./` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export DATABASE_URL=<YOUR_DATABASE_URL>;
export DATABASE_URL_TEST=<YOUR_TMP_DATABASE_URL>;
export AUTH0_DOMAIN=fsnd.au.auth0.com;
export API_AUDIENCE=http://capstone-omc.herokuapp.com/;
export AUTH0_CLIENT_ID=nvEYohEddrdyN3IX0LLyP33S0St7FUc2;
```
To Setup the database run
```bash
python manage.py db migrate
```
To run the server, execute:

```bash
python app.py
```

### Deploying and Hosting on Heroku

Heroku is a cloud platform you can use for free and is a popular tool for smaller companies, those not using AWS, and personal projects.[Heroku Docs](https://devcenter.heroku.com/categories/reference)

Before we can do anything with Heroku, we need to do two things. First, we need to create an account with Heroku [here](https://signup.heroku.com/) 

After you create your account, install Heroku with Homebrew by running:
```sh
brew tap heroku/brew && brew install heroku
```
If you need alternate instructions for the download they can be found [here](https://devcenter.heroku.com/categories/command-line). You can verify the download by typing ```which heroku```.

Once you have the Heroku CLI you can start to run Heroku commands! Enter ```heroku login``` and then provide your authentication information. Now you can start running Heroku commands for your account and applications.
#### Create Heroku App
In order to create the Heroku app run in Bash:
```bash
heroku create name_of_your_app
```
#### Add git remote for Heroku to local repository
Using the git url obtained from the last step, in terminal run:
```bash
git remote add heroku heroku_git_url
```
#### Add postgresql add on for our database
Heroku has an addon for apps for a postgresql database instance. Run this code in order to create your database and connect it to your application: heroku addons:
```bash
create heroku-postgresql:hobby-dev --app name_of_your_application
```

Run ```heroku config --app name_of_your_application``` in order to check your configuration variables in Heroku. You will see DATABASE_URL and the URL of the database you just created.

#### **Push it!**
Push it up!
```bash
git push heroku master
```

#### Run migrations
Once your app is deployed, run migrations by running:
```
heroku run python manage.py db upgrade --app name_of_your_application
```

## Casting Agency API Documentation

### Common Requirements
The following section defines the common requirements For using Casting Agency.

#### Protocol and Calls
Any and all Requests sent to Casting Agency server must use HTTP. Casting Agency APIs can be called using the following:

##### Host
All requests must be sent to the following host: **http://capstone-omc.herokuapp.com/**

##### Methods
- GET
- POST
- DELETE
- PATCH

### Error Handling
Code Values and Error Messages:
- 404: Not Found (the question or the category is not found)
- 422: Un processable.
- 400: Bad request (some of the required data are missing)
- 401: unauthorized
- Errors are returned as JSON in the following format:
```json
{
    'success': False,
    'error': 400,
    'message': 'Bad request'
}
```

### Casting Agency API Objects
The following section details the Casting Agency Objects and their attributes.

#### Movie 
- id: a **Integer**, the question's id
- title: a **String**, the movie's title
- release_date: **Datetime**, the movie's release date

#### Actor
- id: a **Integer**, the actor's id
- name: a **String**, the actor's name
- age: a **Integer**, the actor's age
- gender: a **String**, the actor's gender

### Documentation of API behavior and RBAC controls
#### Roles & Permissions
The Casting Agency have 3 roles each role have permissions
The following text shows the roles and it's permissions
1. Casting Assistant
    - get:actors (show actor in the database)
    - get:movies (show movies in the database)
2. Casting Director
    - All permissions a Casting Assistant has and..
    - add:actor (add new actor to the database)
    - delete:actor (delete actor from the database)
    - edit:actor (edit actor's information)
    - edit:movie (edit movie's information)
3. Executive Producer
    - All permissions a Casting Director has and..
    - delete:movie (delete movie form the database)
    - add:movie (add new movie to the database)
    

#### Authentication & Get JWT
In order to get valid access token you can use ```/auth``` Endpoint which will redirect you to login page.
In file ```./users-password-jwt.txt``` there are users credentials, you can use it to sign in and get access token.

#### Endpoints
- GET '/auth'
- GET '/callback'
- GET '/actors'
- GET '/actors/id'
- DELETE '/actors/id'
- POST '/actors
- PATCH '/actors/id'
- GET '/movies'
- GET '/movies/id'
- DELETE '/movies/id'
- POST '/movies
- PATCH '/movies/id
- POST 'assign'
- DELETE 'assign'

***All the tests are using JWT with Executive Producer role.***

##### GET '/auth'
- Redirect user to login page provided by auth0
- This Endpoint to help the reviewer get the jwt

##### GET '/callback'
- Callback uri contains the access token

##### GET '/actors'
- Fetch a list of all actors in the database
- Request arguments: none
- Returns: Json object with 1 key actor, contains all actors information

**An example url**
```bash
curl --location --request GET 'http://capstone-omc.herokuapp.com/actors' --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw'
```

Response:
```json
{
    "actors": [
        {
            "actor's_information": {
                "age": 70,
                "gender": "male",
                "id": 6,
                "name": "Al Pacino"
            },
            "actor's_movies": {
                "movies": [
                    {
                        "id": 3,
                        "release_date": "Sun, 19 Nov 2000 00:00:00 GMT",
                        "title": "God Father"
                    },
                    {
                        "id": 4,
                        "release_date": "Fri, 19 Nov 2010 00:00:00 GMT",
                        "title": "God Father 2"
                    }
                ]
            }
        },
        {
            "actor's_information": {
                "age": 60,
                "gender": "male",
                "id": 5,
                "name": "Tom Hanks"
            },
            "actor's_movies": {
                "movies": [
                    {
                        "id": 2,
                        "release_date": "Tue, 19 Nov 2002 00:00:00 GMT",
                        "title": "Cast Away"
                    }
                ]
            }
        },
        {
            "actor's_information": {
                "age": 50,
                "gender": "male",
                "id": 7,
                "name": "Will Smith"
            },
            "actor's_movies": {
                "movies": []
            }
        }
    ],
    "success": true
}
```

#### GET 'actors/id'
- Get actor's information
- Request Arguments: id (The actor's id)
- Returns: Json object with 3 keys (actor's_information),(actor's_movies), (success status)

**An example url**
```bash
curl --location --request GET 'http://capstone-omc.herokuapp.com/actors/6' --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw'
```
Response
```json
{
    "actor's_information": {
        "age": 70,
        "gender": "male",
        "id": 6,
        "name": "Al Pacino"
    },
    "actor's_movies": {
        "movies": [
            {
                "id": 3,
                "release_date": "Sun, 19 Nov 2000 00:00:00 GMT",
                "title": "God Father"
            },
            {
                "id": 4,
                "release_date": "Fri, 19 Nov 2010 00:00:00 GMT",
                "title": "God Father 2"
            }
        ]
    },
    "success": true
}
```


#### DELETE '/actors/id'
- Delete an actor
- Request Arguments: id (actor's id).
- Returns : An object with a 2 keys, deleted, that contains the id of the deleted actor, and success message.

**An example url**
```bash
curl --location --request DELETE 'http://capstone-omc.herokuapp.com/actors/7' --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw'
```
Response:
```json
{
    "deleted": 7,
    "success": true
}
```

#### POST '/actor'
- Add new actor to the database
- Request Arguments: None
- Returns: Json object with 2 keys (actor) which contains the new actor's information, and success status

** An example url **
```bash
curl --location --request POST 'http://capstone-omc.herokuapp.com/actors' --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Anglina Jolie",
    "age": 50,
    "gender": "female"
}'
```
Response:
```json
{
    "actor": {
        "age": 50,
        "gender": "female",
        "id": 8,
        "name": "Anglina Jolie"
    },
    "success": true
}
```

#### PATCH '/actor/id'
- edit actor's information
- Request Arguments: id (The actor's id)
- Returns


```json
{
    "actor": {
        "age": 5,
        "gender": "male",
        "id": 6,
        "name": "Al pacino Patch"
    },
    "success": true
}
```

##### GET '/movies'
- Fetch a list of all movies in the database
- Request arguments: none
- Returns: Json object with 1 key movie, contains all movies information

**An example url**
```bash
curl --location --request GET 'http://capstone-omc.herokuapp.com/movies' --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw'
```

Response:
```json
{
    "movies": [
        {
            "movie's_information": {
                "id": 2,
                "release_date": "Tue, 19 Nov 2002 00:00:00 GMT",
                "title": "Cast Away"
            },
            "movie's_movies": {
                "actors": [
                    {
                        "age": 60,
                        "gender": "male",
                        "id": 5,
                        "name": "Tom Hanks"
                    }
                ]
            }
        },
        {
            "movie's_information": {
                "id": 3,
                "release_date": "Sun, 19 Nov 2000 00:00:00 GMT",
                "title": "God Father"
            },
            "movie's_movies": {
                "actors": [
                    {
                        "age": 70,
                        "gender": "male",
                        "id": 6,
                        "name": "Al Pacino"
                    }
                ]
            }
        },
        {
            "movie's_information": {
                "id": 4,
                "release_date": "Fri, 19 Nov 2010 00:00:00 GMT",
                "title": "God Father 2"
            },
            "movie's_movies": {
                "actors": [
                    {
                        "age": 70,
                        "gender": "male",
                        "id": 6,
                        "name": "Al Pacino"
                    }
                ]
            }
        }
    ],
    "success": true
}
```

#### GET 'movies/id'
- Get movie's information
- Request Arguments: id (The movie's id)
- Returns: Json object with 3 keys (movie's_information),(movie's_actors), (success status)

**An example url**
```bash
curl --location --request GET 'http://capstone-omc.herokuapp.com/movies/2' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw'
```
Response
```json
{
    "movie's_actors": {
        "actors": [
            {
                "age": 60,
                "gender": "male",
                "id": 5,
                "name": "Tom Hanks"
            }
        ]
    },
    "movie_information": {
        "id": 2,
        "release_date": "Tue, 19 Nov 2002 00:00:00 GMT",
        "title": "Cast Away"
    },
    "success": true
}
```


#### DELETE '/movie/id'
- Delete an move
- Request Arguments: id (movie's id).
- Returns : An object with a 2 keys, deleted, that contains the id of the deleted movie, and success message.

**An example url**
```bash
curl --location --request DELETE 'http://capstone-omc.herokuapp.com/movies/4' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw'
```
Response:
```json
{
    "deleted": 4,
    "success": true
}
```

#### POST '/movies'
- Add new movie to the database
- Request Arguments: None
- Returns: Json object with 3 keys (movie) which contains the new movie's information, movie's actors, and success status

** An example url **
```bash
curl --location --request POST 'http://capstone-omc.herokuapp.com/movies' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title":"God Father 2",
	"release_date":"2010-11-19"
}'
```
Response:
```json
{{
    "movie": {
        "id": 6,
        "release_date": "Fri, 19 Nov 2010 00:00:00 GMT",
        "title": "God Father 2"
    },
    "movie's_actors": {
        "actors": []
    },
    "success": true
}
```

#### PATCH '/movie/id'
- edit moview's information
- Request Arguments: id (The movie's id)
- Returns
```sh
curl --location --request PATCH 'http://capstone-omc.herokuapp.com/movies/6' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw' \
--header 'Content-Type: application/json' \
--data-raw '{
	"title":"The God Father 1"
}'
```

```json
{
    "movie": {
        "id": 6,
        "title": "The God Father 1",
        "release_date":"Fri, 19 Nov 2010 00:00:00 GMT"
    },
    "success": true
}
```

### POST '/assign'
- Add actor to movie (add relationship between movie and actor)
- Request Arguments: None
- Returns: Json object with 2 keys (movie) which contains the movie information after add the actor to it, and success status

**An example url**
```bash
curl --location --request POST 'http://capstone-omc.herokuapp.com/assign' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw' \
--header 'Content-Type: application/json' \
--data-raw '{
	"movie_id":5,
	"actor_id":8
}'
```
Response
```json
{
    "movie's_actor": {
        "actors": [
            {
                "age": 50,
                "gender": "female",
                "id": 8,
                "name": "Anglina Jolie"
            }
        ]
    },
    "success": true
}
```


### DELETE '/assign'
- Delete actor from movie cast (delete relationship between movie and actor)
- Request Arguments: None
- Returns: Json object with 2 keys (movie) which contains the movie information after delete the actor from it, and success status

**An example url**
```bash
curl --location --request DELETE 'http://capstone-omc.herokuapp.com/assign' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtEeHd5SGE1WUcwR3dmcHVhWWE2SSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYmZjZTY4NmJlNzU3MGJkM2E5MzJiMSIsImF1ZCI6Imh0dHA6Ly9jYXBzdG9uZS1vbWMuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE1ODk4OTc1NzksImV4cCI6MTU4OTk4Mzk3OSwiYXpwIjoibnZFWW9oRWRkcmR5TjNJWDBMTHlQMzNTMFN0N0ZVYzIiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.0Xx26brmGguz1CytFx5GF48YKbOgfi1jWUO54QUILAZeHCek9UrHT_l7uKm_yAFbguHq2-_ipeilRa4hTS3zj6SuniXacSkFZb0GWb6amsjM7xucAo_NT7Pti5qH6XHjAo-HuRpyvKjcyg6moCuVv1Q3AhcETBzOD3-kwmfFJppkxHOi4RhI1n5SoIMVZ7x0LlY9Am2AArwEkWjOUM1UtxdEfc9S8eNTT04zqhyTUzZr0ErS6eXicQ-sQLtFy7LcxidyJg1_WZOIv0bGNjLzCd5XjSST2in34hB5bR8HIfMTCDuhgjjxXx9qg5pv0nsLKTplpaC4KKgYi9L-09E0kw' \
--header 'Content-Type: application/json' \
--data-raw '{
	"movie_id":5,
	"actor_id":8
}'
```
Response
```json
{
    "movie's_actor": {
        "actors": []
    },
    "success": true
}
```
## Testing

### To run the tests:
- Create a temporary Database and run:
```
export DATABASE_URL_TEST=<YOUR-TMP-DB-URL>
```
- Run
```
python test_app.py
```
