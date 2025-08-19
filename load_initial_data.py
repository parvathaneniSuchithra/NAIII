# load_initial_data.py

import json
import os
from database import initialize_firestore # We only need the initializer

# --- Configuration ---
QUESTIONS_JSON_FILE = 'questions_sample.json'
SYLLABUS_JSON_FILE = 'syllabus.json'

# --- Initialize Firestore Connection ---
try:
    db = initialize_firestore()
    print("✅ Firestore connection successful.")
except Exception as e:
    print(f"🔥 Firestore connection failed. Please check your credentials.")
    print(f"   Error: {e}")
    exit()

def get_category_for_quiz(quiz_name):
    """Determines the category for a quiz based on its name."""
    if "SuccessFactors" in quiz_name:
        return "SAP SuccessFactors"
    if "GenAI" in quiz_name:
        return "GenAI & Agentic AI"
    return "SAP Security & GRC"

def load_data():
    """
    Reads JSON files and populates Firestore with categories, users, 
    quizzes, questions, and the complete syllabus.
    This function is safe to run multiple times.
    """
    print("\n--- Starting Database Population ---")

    # --- 1. Create Default User ---
    print("Step 1: Checking for default admin user...")
    if not list(db.collection('users').where('username', '==', 'admin').limit(1).stream()):
        db.collection('users').add({
            'username': 'admin',
            'password': 'admin',
            'role': 'admin',
            'category': 'SAP Security & GRC'
        })
        print("  -> Default 'admin' user created.")
    else:
        print("  -> Admin user already exists.")
    print("Step 1: Complete.")

    # --- 2. Load Quizzes and Questions from JSON File ---
    print(f"\nStep 2: Loading Quizzes and Questions from '{QUESTIONS_JSON_FILE}'...")
    if os.path.exists(QUESTIONS_JSON_FILE):
        with open(QUESTIONS_JSON_FILE, 'r', encoding='utf-8') as f:
            quizzes_data = json.load(f)

        quizzes_ref = db.collection('quizzes')
        categories_ref = db.collection('categories')
        
        # Ensure categories exist
        all_categories = {cat_name for quiz_name, _ in quizzes_data.items() for cat_name in [get_category_for_quiz(quiz_name)]}
        for cat_name in all_categories:
             if not list(categories_ref.where('name', '==', cat_name).limit(1).stream()):
                categories_ref.add({'name': cat_name})
                print(f"  -> Category '{cat_name}' created.")

        for quiz_name, questions in quizzes_data.items():
            if not list(quizzes_ref.where('name', '==', quiz_name).limit(1).stream()):
                category = get_category_for_quiz(quiz_name)
                _, new_quiz_ref = quizzes_ref.add({'name': quiz_name, 'category': category})
                quiz_id = new_quiz_ref.id
                print(f"  -> Added Quiz '{quiz_name}' to category '{category}'.")
                
                questions_subcollection = quizzes_ref.document(quiz_id).collection('questions')
                for q_data in questions:
                    correct_opt = json.dumps(q_data['correct_option']) if isinstance(q_data['correct_option'], list) else q_data['correct_option']
                    questions_subcollection.add({
                        'question_text': q_data['question'],
                        'options': json.dumps(q_data['options']),
                        'correct_option': correct_opt,
                        'explanation': q_data.get('explanation', '')
                    })
                print(f"    - Loaded {len(questions)} questions.")
            else:
                print(f"  -> Quiz '{quiz_name}' already exists. Skipping.")
    else:
        print(f"WARNING: '{QUESTIONS_JSON_FILE}' not found. Skipping quiz loading.")
    print("Step 2: Complete.")


    # --- 3. Load Full Syllabus from syllabus.json ---
    print(f"\nStep 3: Loading Full Syllabus from '{SYLLABUS_JSON_FILE}'...")
    if os.path.exists(SYLLABUS_JSON_FILE):
        with open(SYLLABUS_JSON_FILE, 'r', encoding='utf-8') as f:
            syllabus_data = json.load(f)

        syl_cat_ref = db.collection('syllabus_categories')

        for cat_name, courses in syllabus_data.items():
            # Add syllabus category if it doesn't exist
            cat_query = syl_cat_ref.where('name', '==', cat_name).limit(1).stream()
            category_doc = next(cat_query, None)
            if not category_doc:
                _, category_ref = syl_cat_ref.add({'name': cat_name})
                cat_id = category_ref.id
                print(f"  -> Created syllabus category: '{cat_name}'")
            else:
                cat_id = category_doc.id
                print(f"  -> Syllabus category '{cat_name}' already exists. Verifying content...")

            courses_ref = syl_cat_ref.document(cat_id).collection('courses')
            for course_name, modules in courses.items():
                course_query = courses_ref.where('name', '==', course_name).limit(1).stream()
                course_doc = next(course_query, None)
                if not course_doc:
                    _, course_ref = courses_ref.add({'name': course_name})
                    course_id = course_ref.id
                    print(f"    -> Added course: '{course_name}'")

                    modules_ref = courses_ref.document(course_id).collection('modules')
                    for _, module_data in modules.items():
                        _, module_ref = modules_ref.add({'title': module_data['title']})
                        module_id = module_ref.id
                        
                        lessons_ref = modules_ref.document(module_id).collection('lessons')
                        for lesson_data in module_data['lessons']:
                            lessons_ref.add({
                                'title': lesson_data['title'],
                                'type': lesson_data.get('type', 'lesson')
                            })
                    print(f"      - Added {len(modules)} modules and their lessons.")
                else:
                    print(f"    -> Course '{course_name}' already exists. Skipping.")
    else:
        print(f"WARNING: '{SYLLABUS_JSON_FILE}' not found. Skipping syllabus loading.")
    print("Step 3: Complete.")
    
    print("\n\n✅ Data loading process complete!")

if __name__ == '__main__':
    load_data()