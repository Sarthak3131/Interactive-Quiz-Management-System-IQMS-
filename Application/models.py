from .database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    Full_Name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80),default = 'genral' , nullable=False)
    qualification = db.Column(db.String(80), nullable=False)
    DOB = db.Column(db.String(80), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    
class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', backref='chapter', lazy=True)

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.String(80), nullable=False)
    time_duration = db.Column(db.String(80), nullable=False)
    remarks = db.Column(db.String(80), nullable=True)
    no_of_questions = db.Column(db.Integer,default=0, nullable=False)
    chapter = db.relationship('Chapter', backref='quiz', lazy=True)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    question = db.Column(db.String(80), unique=True, nullable=False)
    option1 = db.Column(db.String(80), nullable=False)
    option2 = db.Column(db.String(80), nullable=False)
    option3 = db.Column(db.String(80), nullable=False)
    option4 = db.Column(db.String(80), nullable=False)
    correct_option = db.Column(db.String(80), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    chapter = db.relationship('Chapter', backref='question', lazy=True)
    quiz = db.relationship('Quiz', backref='question', lazy=True)

class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    attempt_date = db.Column(db.String(80), nullable=False)
    attempt_time = db.Column(db.String(80), nullable=False)
    total_scored = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref='score', lazy=True)
    quiz = db.relationship('Quiz', backref='score', lazy=True)