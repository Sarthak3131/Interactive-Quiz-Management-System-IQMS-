from flask import Flask, request
from flask import render_template,redirect
from flask import current_app as app
from Application.models import *
import json
import random

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            if user.role == 'admin':
                return redirect(f'/admin/{user.id}')
            else:
                return redirect(f'/home/{user.id}')
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        autoincrement = User.query.count()+ 1
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        Full_name = request.form.get('full_name')
        qualification = request.form.get('qualification')
        dob = request.form.get('dob')
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('register.html', error='Email already exists')
        new_user = User(id=autoincrement,username=username, email=email, password=password, Full_Name=Full_name, qualification=qualification, DOB=dob)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/home/'+str(autoincrement))
    return render_template('register.html')

@app.route('/admin/<int:user_id>', methods=['GET', 'POST'])
def admin(user_id):
    user = User.query.filter_by(id=user_id,role="admin").first()
    if user:
        username = user.Full_Name
        quizzes  = Quiz.query.all()
        subjects = Subject.query.all()
        chapters = Chapter.query.all()
        users = User.query.all()
        questions = Question.query.all()
        return render_template('admindashboard.html',username=username,quizzes=quizzes,subjects=subjects,chapters=chapters,user=user,users=users,questions=questions)
    return redirect('/')

@app.route('/home/<int:user_id>', methods=['GET', 'POST'])
def user_dash(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        quizzes  = Quiz.query.all()
        scores = Score.query.filter_by(user_id=user_id).all()
        return render_template('userdashboard.html', user=user, quizzes=quizzes, scores=scores)
    return redirect('/')

@app.route('/admin/create-quiz', methods=['POST'])
def create_quiz():
    admin_id = Admin.query.first().id
    if request.method == 'POST':
        r_id = random.randint(1,100)
        while Subject.query.filter_by(id=r_id).first():
            r_id = random.randint(1,100)
        autoincrement = r_id
        chapter_id = request.form.get('chapter_id')
        date_of_quiz = request.form.get('date_of_quiz')
        time_duration = request.form.get('time_duration')
        remarks = request.form.get('remarks')
        new_quiz = Quiz(id=autoincrement,chapter_id=chapter_id, date_of_quiz=date_of_quiz, time_duration=time_duration, remarks=remarks)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(f'/admin/{admin_id}')

@app.route('/admin/add-subject', methods=['POST'])
def add_subject():
    admin_id = Admin.query.first().id
    if request.method == 'POST':
        r_id = random.randint(1,100)
        while Subject.query.filter_by(id=r_id).first():
            r_id = random.randint(1,100)
        autoincrement = r_id
        name = request.form.get('sname')
        description = request.form.get('sdescription')
        new_subject = Subject(id=autoincrement,name=name, description=description)
        db.session.add(new_subject)
        db.session.commit()
        return redirect(f'/admin/{admin_id}')

@app.route('/admin/add-chapter', methods=['POST'])
def add_chapter():
    admin_id = Admin.query.first().id
    if request.method == 'POST':
        r_id = random.randint(1,100)
        while Chapter.query.filter_by(id=r_id).first():
            r_id = random.randint(1,100)
        autoincrement = r_id
        name = request.form.get('cname')
        description = request.form.get('cdescription')
        subject_id = request.form.get('subject_id')
        new_chapter = Chapter(id=autoincrement,name=name, description=description, subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(f'/admin/{admin_id}')

@app.route('/admin/add-questions', methods=['POST'])
def add_question():
    admin_id = Admin.query.first().id
    if request.method == 'POST':
        r_id = random.randint(1,100)
        while Question.query.filter_by(id=r_id).first():
            r_id = random.randint(1,100)
        autoincrement = r_id
        question = request.form.get('question')
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')
        option4 = request.form.get('option4')
        correct_option = request.form.get('correctAnswer')
        if correct_option == '1' :
            correct_option = option1
        elif correct_option == '2' :
            correct_option = option2
        elif correct_option == '3' :
            correct_option = option3
        elif correct_option == '4' :
            correct_option = option4
        quiz_id = request.form.get('quiz_id')
        chapter_id = Quiz.query.filter_by(id=quiz_id).first().chapter_id
        new_question = Question(id=autoincrement,question=question, option1=option1, option2=option2, option3=option3, option4=option4, correct_option=correct_option, chapter_id=chapter_id, quiz_id=quiz_id)
        db.session.add(new_question)
        db.session.commit()
        no_of_questions = Question.query.filter_by(quiz_id=quiz_id).count()
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        quiz.no_of_questions = no_of_questions
        db.session.commit()
        return redirect(f'/admin/{admin_id}')
    
@app.route('/quizpage/<int:quiz_id>/<int:user_id>', methods=['GET', 'POST'])
def quizpage(quiz_id,user_id):
    user = User.query.filter_by(id=user_id).first()
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    quest = Question.query.filter_by(quiz_id=quiz_id).all()
    quiz_questions = [{"question":q.question,"options":[q.option1,q.option2,q.option3,q.option4],"answer": q.correct_option  } for q in quest]
    quiz_questions_json = json.dumps(quiz_questions)
    time = quiz.time_duration
    hours, minutes = time.split(":")
    timehr = int(hours)
    timemin = int(minutes)
    time_duration = timehr*60*60 + timemin*60
    if user and quiz:
        return render_template('quizpage.html', user=user, quiz=quiz, quiz_questions=quiz_questions_json, time_duration=time_duration)
    return redirect('/')

@app.route('/save-score/<int:quiz_id>/<int:user_id>', methods=['POST'])
def save_score(quiz_id,user_id):
    user = User.query.filter_by(id=user_id).first()
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    if user and quiz:
        r_id = random.randint(1,100)
        while Score.query.filter_by(id=r_id).first():
            r_id = random.randint(1,100)
        autoincrement = r_id
        score = request.form.get('totalQuestions')
        time_stamp_of_attempt = request.form.get('attemptTime')
        total_scored = request.form.get('finalScore')
        attempt_date = time_stamp_of_attempt[0:10]
        attempt_time = time_stamp_of_attempt[11:16]
        new_score = Score(id=autoincrement,user_id=user_id, quiz_id=quiz_id, score=score, attempt_date=attempt_date, attempt_time=attempt_time, total_scored=total_scored)
        db.session.add(new_score)
        db.session.commit()
        return redirect(f'/home/{user_id}')
    return redirect('/')

@app.route('/admin/edit-quiz', methods=['POST'])
def edit_quiz():
    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')
        date_of_quiz = request.form.get('date_of_quiz')
        time_duration = request.form.get('time_duration')
        remarks = request.form.get('remarks')
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        quiz.date_of_quiz = date_of_quiz
        quiz.time_duration = time_duration
        quiz.remarks = remarks
        db.session.commit()
        return redirect(f'/admin/1')

@app.route('/admin/edit-subject', methods=['POST'])
def edit_subject():
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        name = request.form.get('sname')
        description = request.form.get('sdescription')
        print(subject_id,name,description)
        subject = Subject.query.filter_by(id=subject_id).first()
        subject.name = name
        subject.description = description
        db.session.commit()
        return redirect(f'/admin/1')

@app.route('/admin/edit-chapter', methods=['POST'])
def edit_chapter():
    if request.method == 'POST':
        chapter_id = request.form.get('chapter_id')
        name = request.form.get('cname')
        description = request.form.get('cdescription')
        chapter = Chapter.query.filter_by(id=chapter_id).first()
        chapter.name = name
        chapter.description = description
        db.session.commit()
        return redirect(f'/admin/1')

@app.route('/admin/delete-quiz', methods=['POST'])
def delete_quiz():
    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')

        # Delete related scores
        scores = Score.query.filter_by(quiz_id=quiz_id).all()
        for score in scores:
            db.session.delete(score)
        db.session.commit()

        # Delete related questions
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        for question in questions:
            db.session.delete(question)
        db.session.commit()

        # Delete the quiz
        quiz = Quiz.query.get(quiz_id)
        if quiz:
            db.session.delete(quiz)
            db.session.commit()

        return redirect('/admin/1')

@app.route('/admin/delete-subject', methods=['POST'])
def delete_subject():
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')

        # Delete related scores
        scores = Score.query.join(Quiz).join(Chapter).filter(Chapter.subject_id == subject_id).all()
        for score in scores:
            db.session.delete(score)
        db.session.commit()

        # Delete related questions
        questions = Question.query.join(Quiz).join(Chapter).filter(Chapter.subject_id == subject_id).all()
        for question in questions:
            db.session.delete(question)
        db.session.commit()

        # Delete related quizzes
        quizzes = Quiz.query.join(Chapter).filter(Chapter.subject_id == subject_id).all()
        for quiz in quizzes:
            db.session.delete(quiz)
        db.session.commit()

        # Delete related chapters
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        for chapter in chapters:
            db.session.delete(chapter)
        db.session.commit()

        # Delete the subject
        subject = Subject.query.get(subject_id)
        if subject:
            db.session.delete(subject)
            db.session.commit()

        return redirect('/admin/1')

@app.route('/admin/delete-chapter', methods=['POST'])
def delete_chapter():
    if request.method == 'POST':
        chapter_id = request.form.get('chapter_id')

        # Delete related scores
        scores = Score.query.join(Quiz).filter(Quiz.chapter_id == chapter_id).all()
        for score in scores:
            db.session.delete(score)
        db.session.commit()

        # Delete related questions
        questions = Question.query.filter_by(chapter_id=chapter_id).all()
        for question in questions:
            db.session.delete(question)
        db.session.commit()

        # Delete related quizzes
        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        for quiz in quizzes:
            db.session.delete(quiz)
        db.session.commit()

        # Delete the chapter
        chapter = Chapter.query.get(chapter_id)
        if chapter:
            db.session.delete(chapter)
            db.session.commit()

        return redirect('/admin/1')