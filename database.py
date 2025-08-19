# database.py

import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

def initialize_firestore():
    """
    Initializes Firestore connection.
    Uses Streamlit secrets when deployed, otherwise uses the local
    GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    if not firebase_admin._apps:
        # Check if running in Streamlit Cloud and secrets are set
        if 'firestore' in st.secrets:
            creds_dict = dict(st.secrets.firestore)
            cred = credentials.Certificate(creds_dict)
        # Fallback to local development using Application Default Credentials
        else:
            cred = credentials.ApplicationDefault()

        firebase_admin.initialize_app(cred, {
            'projectId': 'nvai-469312', # Your specific Project ID
        })
    return firestore.client()

db = initialize_firestore()

# --- User Management ---
def get_user(username):
    """Fetches a user from Firestore by username."""
    query = db.collection('users').where('username', '==', username).limit(1).stream()
    for user in query:
        user_data = user.to_dict()
        user_data['id'] = user.id
        return user_data
    return None

def add_user(username, password, role, category):
    """Adds a new user to Firestore."""
    db.collection('users').add({
        'username': username,
        'password': password,
        'role': role,
        'category': category
    })

def get_all_users():
    """Retrieves all users from Firestore."""
    users_stream = db.collection('users').stream()
    return [{'id': user.id, **user.to_dict()} for user in users_stream]

def update_user(user_id, new_username, new_category):
    """Updates a user's details in Firestore."""
    db.collection('users').document(user_id).update({
        'username': new_username,
        'category': new_category
    })

def delete_user(user_id):
    """Deletes a user from Firestore."""
    db.collection('users').document(user_id).delete()

# --- Category Management ---
def get_categories():
    """Retrieves all user/quiz categories from Firestore."""
    categories_stream = db.collection('categories').stream()
    return [{'id': cat.id, **cat.to_dict()} for cat in categories_stream]

def add_category(category_name):
    """Adds a new category to Firestore if it doesn't exist."""
    if not list(db.collection('categories').where('name', '==', category_name).limit(1).stream()):
        db.collection('categories').add({'name': category_name})

def update_category(category_id, new_name):
    """Updates a category name in Firestore."""
    db.collection('categories').document(category_id).update({'name': new_name})

def delete_category(category_id):
    """Deletes a category from Firestore."""
    db.collection('categories').document(category_id).delete()

# --- Quiz Management ---
def get_quizzes_by_category(category):
    """Gets all quizzes for a specific category from Firestore."""
    quizzes_stream = db.collection('quizzes').where('category', '==', category).stream()
    return [{'id': quiz.id, **quiz.to_dict()} for quiz in quizzes_stream]

def get_all_quizzes():
    """Gets all quizzes from Firestore."""
    quizzes_stream = db.collection('quizzes').stream()
    return [{'id': quiz.id, **quiz.to_dict()} for quiz in quizzes_stream]

def add_quiz(name, category):
    """Adds a new quiz to Firestore. Returns the new quiz ID or None if it already exists."""
    if list(db.collection('quizzes').where('name', '==', name).limit(1).stream()):
        return None 
    _, new_quiz_ref = db.collection('quizzes').add({'name': name, 'category': category})
    return new_quiz_ref.id

# --- Question Management (Complete) ---
def get_questions_for_quiz(quiz_id):
    """Retrieves all questions for a given quiz ID from Firestore."""
    questions_stream = db.collection('quizzes').document(quiz_id).collection('questions').stream()
    return [{'id': q.id, **q.to_dict()} for q in questions_stream]

def add_question(quiz_id, question_text, options, correct_option, explanation):
    """Adds a question to a specific quiz in Firestore."""
    db.collection('quizzes').document(quiz_id).collection('questions').add({
        'question_text': question_text, 'options': json.dumps(options),
        'correct_option': correct_option, 'explanation': explanation
    })
    
def update_question(quiz_id, question_id, new_text, new_options, new_correct, new_explanation):
    """Updates an existing question."""
    db.collection('quizzes').document(quiz_id).collection('questions').document(question_id).update({
        'question_text': new_text, 'options': json.dumps(new_options),
        'correct_option': new_correct, 'explanation': new_explanation
    })

def delete_question(quiz_id, question_id):
    """Deletes a question from a specific quiz."""
    db.collection('quizzes').document(quiz_id).collection('questions').document(question_id).delete()

# --- User Progress Management ---
def save_user_progress(user_id, quiz_id, score, total, completed, answers_log):
    """Saves a user's quiz progress in Firestore."""
    quiz_doc = db.collection('quizzes').document(quiz_id).get()
    quiz_name = quiz_doc.to_dict().get('name', 'Unknown Quiz') if quiz_doc.exists else "Unknown Quiz"
    db.collection('user_progress').add({
        'user_id': user_id, 'quiz_id': quiz_id, 'quiz_name': quiz_name,
        'score': score, 'total': total, 'completed': completed,
        'answers_log': json.dumps(answers_log), 'timestamp': firestore.SERVER_TIMESTAMP
    })

def get_user_progress(user_id):
    """Gets all progress records for a specific user."""
    progress_stream = db.collection('user_progress').where('user_id', '==', user_id).stream()
    progress = []
    for record in progress_stream:
        p_data = record.to_dict()
        p_data['id'] = record.id
        if p_data.get('timestamp'):
             p_data['timestamp'] = p_data['timestamp'].timestamp()
        progress.append(p_data)
    return progress

def get_all_user_progress():
    """Retrieves a comprehensive and efficient performance report for all users."""
    users_stream = db.collection('users').stream()
    users_map = {user.id: user.to_dict().get('username', 'Unknown') for user in users_stream}
    quizzes_stream = db.collection('quizzes').stream()
    quizzes_map = {quiz.id: quiz.to_dict() for quiz in quizzes_stream}
    progress_stream = db.collection('user_progress').stream()
    full_progress_data = []
    for record in progress_stream:
        p_data = record.to_dict()
        p_data['id'] = record.id
        p_data['username'] = users_map.get(p_data.get('user_id'), 'Unknown User')
        quiz_details = quizzes_map.get(p_data.get('quiz_id'))
        if quiz_details:
            p_data['quiz_name'] = quiz_details.get('name', 'Unknown Quiz')
            p_data['category'] = quiz_details.get('category', 'Uncategorized')
        else:
            p_data['quiz_name'] = 'Unknown Quiz'
            p_data['category'] = 'Uncategorized'
        if p_data.get('timestamp'):
             p_data['timestamp'] = p_data['timestamp'].timestamp()
        full_progress_data.append(p_data)
    return full_progress_data

# --- Syllabus Management (Complete) ---
def add_syllabus_category(name):
    """Adds a new syllabus category if it doesn't already exist."""
    if not list(db.collection('syllabus_categories').where('name', '==', name).limit(1).stream()):
        db.collection('syllabus_categories').add({'name': name})

def get_syllabus_categories():
    """Retrieves all syllabus categories."""
    categories_stream = db.collection('syllabus_categories').stream()
    return [{'id': cat.id, **cat.to_dict()} for cat in categories_stream]

def update_syllabus_category(category_id, new_name):
    """Updates a syllabus category's name."""
    db.collection('syllabus_categories').document(category_id).update({'name': new_name})

def delete_syllabus_category(category_id):
    """Deletes a syllabus category."""
    db.collection('syllabus_categories').document(category_id).delete()

def add_syllabus_course(name, category_id):
    """Adds a new course to a syllabus category."""
    courses_ref = db.collection('syllabus_categories').document(category_id).collection('courses')
    if not list(courses_ref.where('name', '==', name).limit(1).stream()):
        courses_ref.add({'name': name})

def get_syllabus_courses(category_id):
    """Retrieves all courses for a syllabus category."""
    courses_stream = db.collection('syllabus_categories').document(category_id).collection('courses').stream()
    return [{'id': course.id, **course.to_dict()} for course in courses_stream]

def add_syllabus_module(title, category_id, course_id):
    """Adds a new module to a course."""
    modules_ref = db.collection('syllabus_categories').document(category_id).collection('courses').document(course_id).collection('modules')
    if not list(modules_ref.where('title', '==', title).limit(1).stream()):
        modules_ref.add({'title': title})

def get_syllabus_modules(category_id, course_id):
    """Retrieves all modules for a course."""
    modules_stream = db.collection('syllabus_categories').document(category_id).collection('courses').document(course_id).collection('modules').stream()
    return [{'id': mod.id, **mod.to_dict()} for mod in modules_stream]

def add_syllabus_lesson(title, lesson_type, category_id, course_id, module_id):
    """Adds a new lesson to a module."""
    db.collection('syllabus_categories').document(category_id).collection('courses').document(course_id).collection('modules').document(module_id).collection('lessons').add({'title': title, 'type': lesson_type})

def get_syllabus_lessons(category_id, course_id, module_id):
    """Retrieves all lessons for a module."""
    lessons_stream = db.collection('syllabus_categories').document(category_id).collection('courses').document(course_id).collection('modules').document(module_id).collection('lessons').stream()
    return [{'id': lesson.id, **lesson.to_dict()} for lesson in lessons_stream]