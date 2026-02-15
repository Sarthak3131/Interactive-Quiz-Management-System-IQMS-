from flask_restful import Resource
from Application.database import db

class SubjectAPI(Resource):
    def get(self, name):
        subject = db.session.query(Subject).filter_by(name=name).first()
        if subject:
            return {'Subject_ID': subject.id,'Name': subject.name, 'Description': subject.description}
        else:
            return {'message': 'Subject not found'}, 404

class ChapterAPI(Resource):
    def get(self, name):
        chapter = db.session.query(Chapter).filter_by(name=name).first()
        if chapter:
            return {'Chapter_ID': chapter.id,'Name': chapter.name, 'Description': chapter.description}
        else:
            return {'message': 'Chapter not found'}, 404

class QuizAPI(Resource):
    def get(self, id):
        quiz = db.session.query(Quiz).filter_by(id=id).first()
        if quiz:
            return {'Quiz_ID': quiz.id,'Chapter_ID': quiz.chapter_id, 'Date_of_Quiz': quiz.date_of_quiz, 'Time_Duration': quiz.time_duration, 'Remarks': quiz.remarks, 'No_of_Questions': quiz.no_of_questions}
        else:
            return {'message': 'Quiz not found'}, 404

class ScoresAPI(Resource):
    def get(self, id):
        score = db.session.query(Score).filter_by(id=id).first()
        if score:
            return {'Score_ID': score.id,'User_ID': score.user_id}
        else:
            return {'message': 'Score not found'}, 404