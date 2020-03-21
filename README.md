## Todo application

### Motivation
The objective of creating this application is to learn following skills:
1. Creating RESTful API endpoints in Flask.(**Flask web framework**)
2. Querying and manipulating databases in order to serve endpoints.(**Flask-SQLAlchemy** and **postgresql**)
3. Modeling Many-to-one database relationships between models.(**Referential integrity**)
4. Changing database schema in the middle of creating applications and let migrations(**Flask-migrate**) do the part of updating schema.
5. Sending data to template and rendering the data.(**HTML, CSS, javascript**)
6. Using jinja template to inject python in HTML.(**jinja**)
7. Taking user input from forms and updating data asyncronuously using **fetch** library.

### API endpoints
This application serves following endpoints:
1. POST  /lists/<list_id>/todos/create
2. POST /todos/<todo_id>/set-completed
3. POST /lists/<list_id>/list-completed
4. DELETE /todos/<todo_id>
5. DELETE /lists/<list_id>
6. GET /lists/<list_id>
7. POST /lists/create

### Development Setup
```
cd <project directory>
```
```
export FLASK_APP=app.py
export DEBUG_ENV=development
flask run
```
Navigate to Home page: http://localhost:5000
