import sqlite3
import json
import time

DATABASE_FILE = "quiz_app.db"

def get_db_connection():
    """
    Establishes a connection to the SQLite database.
    - Enables row_factory for name-based column access.
    - Enforces foreign key constraints.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    """Creates all necessary database tables if they don't already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # --- User, Quiz, and Category Tables ---
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT, category TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS quizzes (id INTEGER PRIMARY KEY, name TEXT UNIQUE, category TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, quiz_id INTEGER, question_text TEXT, options TEXT, correct_option TEXT, explanation TEXT, FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE)")
    
    # --- IMPROVEMENT: Added timestamp column to user_progress ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY, 
            user_id INTEGER, 
            quiz_id INTEGER, 
            score INTEGER, 
            total INTEGER, 
            attempted BOOLEAN, 
            answers_log TEXT, 
            timestamp INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE, 
            FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE, 
            UNIQUE(user_id, quiz_id)
        )
    """)
    
    # --- Syllabus Tables ---
    cursor.execute("CREATE TABLE IF NOT EXISTS syllabus_categories (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS syllabus_courses (id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER, FOREIGN KEY (category_id) REFERENCES syllabus_categories (id) ON DELETE CASCADE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS syllabus_modules (id INTEGER PRIMARY KEY, title TEXT, course_id INTEGER, FOREIGN KEY (course_id) REFERENCES syllabus_courses (id) ON DELETE CASCADE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS syllabus_lessons (id INTEGER PRIMARY KEY, title TEXT, type TEXT, module_id INTEGER, FOREIGN KEY (module_id) REFERENCES syllabus_modules (id) ON DELETE CASCADE)")
    
    conn.commit()
    conn.close()

# --- Category Management ---
def add_category(name):
    """Adds a new user/quiz category."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        conn.commit()

def get_categories():
    """Retrieves all user/quiz categories."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM categories ORDER BY name").fetchall()

def delete_category(category_id):
    """Deletes a user/quiz category."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()

def update_category(category_id, new_name):
    """Updates the name of a user/quiz category."""
    with get_db_connection() as conn:
        conn.execute("UPDATE categories SET name = ? WHERE id = ?", (new_name, category_id))
        conn.commit()

# --- User Management ---
def add_user(username, password, role, category=None):
    """Adds a new user."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO users (username, password, role, category) VALUES (?, ?, ?, ?)", (username, password, role, category))
        conn.commit()

def get_user(username):
    """Retrieves a single user by username."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

def get_all_users():
    """Retrieves all users."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM users ORDER BY username").fetchall()

def delete_user(user_id):
    """Deletes a user."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

def update_user(user_id, new_username, new_category):
    """Updates a user's details."""
    with get_db_connection() as conn:
        conn.execute("UPDATE users SET username = ?, category = ? WHERE id = ?", (new_username, new_category, user_id))
        conn.commit()

# --- Quiz Management ---
def add_quiz(name, category):
    """Adds a new quiz."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO quizzes (name, category) VALUES (?, ?)", (name, category))
        conn.commit()

def get_all_quizzes():
    """Retrieves all quizzes."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM quizzes ORDER BY category, name").fetchall()

def get_quizzes_by_category(category):
    """Retrieves all quizzes for a specific category."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM quizzes WHERE category = ? ORDER BY name", (category,)).fetchall()

# --- Question Management ---
def add_question(quiz_id, question_text, options, correct_option, explanation):
    """Adds a new question to a quiz."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO questions (quiz_id, question_text, options, correct_option, explanation) VALUES (?, ?, ?, ?, ?)",
                     (quiz_id, question_text, json.dumps(options), correct_option, explanation))
        conn.commit()

def get_questions_for_quiz(quiz_id):
    """Retrieves all questions for a specific quiz."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,)).fetchall()

def update_question(question_id, new_text, new_options, new_correct, new_explanation):
    """Updates an existing question."""
    with get_db_connection() as conn:
        conn.execute("UPDATE questions SET question_text = ?, options = ?, correct_option = ?, explanation = ? WHERE id = ?",
                     (new_text, json.dumps(new_options), new_correct, new_explanation, question_id))
        conn.commit()

def delete_question(question_id):
    """Deletes a question."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()

# --- User Progress Management ---
def save_user_progress(user_id, quiz_id, score, total, attempted, answers_log):
    """
    **IMPROVED**: Saves or updates a user's quiz progress using an efficient 'UPSERT' operation.
    Now includes a timestamp for tracking trends.
    """
    conn = get_db_connection()
    timestamp = int(time.time())
    # Using modern UPSERT syntax for efficiency
    conn.execute("""
        INSERT INTO user_progress (user_id, quiz_id, score, total, attempted, answers_log, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id, quiz_id) DO UPDATE SET
            score = excluded.score,
            total = excluded.total,
            attempted = excluded.attempted,
            answers_log = excluded.answers_log,
            timestamp = excluded.timestamp
    """, (user_id, quiz_id, score, total, attempted, json.dumps(answers_log), timestamp))
    conn.commit()
    conn.close()

def get_user_progress(user_id):
    """
    **IMPROVED**: Retrieves a specific user's progress, now including the timestamp.
    """
    with get_db_connection() as conn:
        return conn.execute("""
            SELECT up.*, q.name as quiz_name 
            FROM user_progress up 
            JOIN quizzes q ON up.quiz_id = q.id 
            WHERE up.user_id = ?
            ORDER BY up.timestamp DESC
        """, (user_id,)).fetchall()

def get_all_user_progress():
    """
    **IMPROVED**: Retrieves a comprehensive performance report for all users.
    This single query provides all data needed for the admin dashboard.
    """
    with get_db_connection() as conn:
        return conn.execute("""
            SELECT 
                u.username, 
                q.name as quiz_name, 
                q.category,
                up.score, 
                up.total,
                up.timestamp
            FROM user_progress up 
            JOIN users u ON up.user_id = u.id 
            JOIN quizzes q ON up.quiz_id = q.id 
            WHERE up.attempted = 1 
            ORDER BY up.timestamp DESC
        """).fetchall()

# --- Syllabus Management (Complete CRUD) ---
def add_syllabus_category(name):
    """Adds a new syllabus category."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO syllabus_categories (name) VALUES (?)", (name,))
        conn.commit()

def get_syllabus_categories():
    """Retrieves all syllabus categories."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM syllabus_categories ORDER BY name").fetchall()

def update_syllabus_category(category_id, new_name):
    """Updates a syllabus category's name."""
    with get_db_connection() as conn:
        conn.execute("UPDATE syllabus_categories SET name = ? WHERE id = ?", (new_name, category_id))
        conn.commit()

def delete_syllabus_category(category_id):
    """Deletes a syllabus category."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM syllabus_categories WHERE id = ?", (category_id,))
        conn.commit()

def add_syllabus_course(name, category_id):
    """Adds a new course to a syllabus category."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO syllabus_courses (name, category_id) VALUES (?, ?)", (name, category_id))
        conn.commit()

def get_syllabus_courses(category_id):
    """Retrieves all courses for a syllabus category."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM syllabus_courses WHERE category_id = ? ORDER BY name", (category_id,)).fetchall()

def update_syllabus_course(course_id, new_name):
    """Updates a course's name."""
    with get_db_connection() as conn:
        conn.execute("UPDATE syllabus_courses SET name = ? WHERE id = ?", (new_name, course_id))
        conn.commit()

def delete_syllabus_course(course_id):
    """Deletes a course."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM syllabus_courses WHERE id = ?", (course_id,))
        conn.commit()

def add_syllabus_module(title, course_id):
    """Adds a new module to a course."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO syllabus_modules (title, course_id) VALUES (?, ?)", (title, course_id))
        conn.commit()

def get_syllabus_modules(course_id):
    """Retrieves all modules for a course."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM syllabus_modules WHERE course_id = ? ORDER BY id", (course_id,)).fetchall()

def update_syllabus_module(module_id, new_title):
    """Updates a module's title."""
    with get_db_connection() as conn:
        conn.execute("UPDATE syllabus_modules SET title = ? WHERE id = ?", (new_title, module_id))
        conn.commit()

def delete_syllabus_module(module_id):
    """Deletes a module."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM syllabus_modules WHERE id = ?", (module_id,))
        conn.commit()

def add_syllabus_lesson(title, type, module_id):
    """Adds a new lesson to a module."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO syllabus_lessons (title, type, module_id) VALUES (?, ?, ?)", (title, type, module_id))
        conn.commit()

def get_syllabus_lessons(module_id):
    """Retrieves all lessons for a module."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM syllabus_lessons WHERE module_id = ? ORDER BY id", (module_id,)).fetchall()

def update_syllabus_lesson(lesson_id, new_title, new_type):
    """Updates a lesson's details."""
    with get_db_connection() as conn:
        conn.execute("UPDATE syllabus_lessons SET title = ?, type = ? WHERE id = ?", (new_title, new_type, lesson_id))
        conn.commit()

def delete_syllabus_lesson(lesson_id):
    """Deletes a lesson."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM syllabus_lessons WHERE id = ?", (lesson_id,))
        conn.commit()