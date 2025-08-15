import sqlite3
import json
import time

# Standardized database filename
DATABASE_FILE = "quiz_database.db"

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
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT, category TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS quizzes (id INTEGER PRIMARY KEY, name TEXT UNIQUE, category TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, quiz_id INTEGER, question_text TEXT, options TEXT, correct_option TEXT, explanation TEXT, FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE)")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER NOT NULL, 
                quiz_id INTEGER NOT NULL, 
                quiz_name TEXT,
                score INTEGER NOT NULL, 
                total INTEGER NOT NULL, 
                completed BOOLEAN NOT NULL, 
                answers_log TEXT, 
                timestamp INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE, 
                FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE
            )
        """)
        cursor.execute("CREATE TABLE IF NOT EXISTS syllabus_categories (id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS syllabus_courses (id INTEGER PRIMARY KEY, name TEXT, category_id INTEGER, FOREIGN KEY (category_id) REFERENCES syllabus_categories (id) ON DELETE CASCADE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS syllabus_modules (id INTEGER PRIMARY KEY, title TEXT, course_id INTEGER, FOREIGN KEY (course_id) REFERENCES syllabus_courses (id) ON DELETE CASCADE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS syllabus_lessons (id INTEGER PRIMARY KEY, title TEXT, type TEXT, module_id INTEGER, FOREIGN KEY (module_id) REFERENCES syllabus_modules (id) ON DELETE CASCADE)")
        conn.commit()

# --- Category Management ---
def add_category(name):
    """Adds a new user/quiz category."""
    with get_db_connection() as conn:
        conn.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
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
    """Adds a new quiz. Returns the new quiz ID or None if it already exists."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO quizzes (name, category) VALUES (?, ?)", (name, category))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

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
    """Adds a new question to a quiz, correctly handling list and string types for the answer."""
    with get_db_connection() as conn:
        options_str = json.dumps(options)
        correct_option_str = json.dumps(correct_option) if isinstance(correct_option, list) else correct_option
        
        conn.execute("INSERT INTO questions (quiz_id, question_text, options, correct_option, explanation) VALUES (?, ?, ?, ?, ?)",
                     (quiz_id, question_text, options_str, correct_option_str, explanation))
        conn.commit()


def get_questions_for_quiz(quiz_id):
    """Retrieves all questions for a specific quiz."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,)).fetchall()

def update_question(question_id, new_text, new_options, new_correct, new_explanation):
    """Updates an existing question, correctly handling list and string types."""
    with get_db_connection() as conn:
        options_str = json.dumps(new_options)
        correct_str = json.dumps(new_correct) if isinstance(new_correct, list) else new_correct

        conn.execute("UPDATE questions SET question_text = ?, options = ?, correct_option = ?, explanation = ? WHERE id = ?",
                     (new_text, options_str, correct_str, new_explanation, question_id))
        conn.commit()

def delete_question(question_id):
    """Deletes a question."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()

# --- User Progress Management ---
def save_user_progress(user_id, quiz_id, score, total, completed, answers_log):
    """Saves a user's quiz progress, including a timestamp."""
    with get_db_connection() as conn:
        quiz_name = conn.execute("SELECT name FROM quizzes WHERE id = ?", (quiz_id,)).fetchone()['name']
        log_str = json.dumps(answers_log)
        timestamp = int(time.time())
        
        conn.execute("""
            INSERT INTO user_progress (user_id, quiz_id, quiz_name, score, total, completed, answers_log, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, quiz_id, quiz_name, score, total, completed, log_str, timestamp))
        conn.commit()

def get_user_progress(user_id):
    """Retrieves a specific user's progress, including the timestamp."""
    with get_db_connection() as conn:
        return conn.execute("""
            SELECT up.*, q.name as quiz_name 
            FROM user_progress up 
            JOIN quizzes q ON up.quiz_id = q.id 
            WHERE up.user_id = ?
            ORDER BY up.timestamp DESC
        """, (user_id,)).fetchall()

def get_all_user_progress():
    """Retrieves a comprehensive performance report for all users."""
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
            WHERE up.completed = 1 
            ORDER BY up.timestamp DESC
        """).fetchall()

# --- Syllabus Management ---
def add_syllabus_category(name):
    """Adds a new syllabus category."""
    with get_db_connection() as conn:
        conn.execute("INSERT OR IGNORE INTO syllabus_categories (name) VALUES (?)", (name,))
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

def add_syllabus_module(title, course_id):
    """Adds a new module to a course."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO syllabus_modules (title, course_id) VALUES (?, ?)", (title, course_id))
        conn.commit()

def get_syllabus_modules(course_id):
    """Retrieves all modules for a course."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM syllabus_modules WHERE course_id = ? ORDER BY id", (course_id,)).fetchall()

def add_syllabus_lesson(title, type, module_id):
    """Adds a new lesson to a module."""
    with get_db_connection() as conn:
        conn.execute("INSERT INTO syllabus_lessons (title, type, module_id) VALUES (?, ?, ?)", (title, type, module_id))
        conn.commit()

def get_syllabus_lessons(module_id):
    """Retrieves all lessons for a module."""
    with get_db_connection() as conn:
        return conn.execute("SELECT * FROM syllabus_lessons WHERE module_id = ? ORDER BY id", (module_id,)).fetchall()
