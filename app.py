from flask import Flask
from Application.database import db
from flask_restful import Resource, Api
app = None
api = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///quizmaster.sqlite3"
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app, api

app, api = create_app()
from Application.controller import *
from Application.api import *
api.add_resource(SubjectAPI, '/api/subject/<string:name>')
api.add_resource(ChapterAPI, '/api/chapter/<string:name>')
api.add_resource(QuizAPI, '/api/quiz/<int:id>')
api.add_resource(ScoresAPI, '/api/score/<int:id>')

if __name__ == '__main__':
    app.run()