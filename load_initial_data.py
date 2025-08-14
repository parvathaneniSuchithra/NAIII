import json
import database as db
import os

# --- Configuration ---
QUESTIONS_JSON_FILE = 'questions_sample.json'
# The script will create these categories for quizzes and users
USER_QUIZ_CATEGORIES = ["SAP Security & GRC", "SAP SuccessFactors", "GenAI & Agentic AI"]

def get_category_for_quiz(quiz_name):
    """
    Determines the appropriate quiz category based on keywords in the quiz name.
    This makes the script adaptable to the varied quizzes in the JSON file.

    Args:
        quiz_name (str): The name of the quiz.

    Returns:
        str: The determined category name.
    """
    if "SuccessFactors" in quiz_name:
        return "SAP SuccessFactors"
    if "GenAI" in quiz_name:
        return "GenAI & Agentic AI"
    # Default category for SAP Security, GRC, and other related quizzes
    return "SAP Security & GRC"

def load_initial_data():
    """
    Reads the questions JSON file and pre-defined syllabus to load all initial data
    into the database. It now intelligently assigns quizzes to the correct category.
    """
    
    print("Initializing database tables...")
    db.create_tables()
    
    # --- Create User/Quiz Categories ---
    print("\n--- Creating User/Quiz Categories ---")
    for cat_name in USER_QUIZ_CATEGORIES:
        try:
            db.add_category(cat_name)
            print(f"-> Category '{cat_name}' created.")
        except Exception:
            print(f"-> Category '{cat_name}' likely already exists. Skipping.")

    # --- Load Quizzes and Questions ---
    print(f"\n--- Loading Quizzes from '{QUESTIONS_JSON_FILE}' ---")
    if os.path.exists(QUESTIONS_JSON_FILE):
        with open(QUESTIONS_JSON_FILE, 'r', encoding='utf-8') as f:
            quizzes_data = json.load(f)

        for quiz_name, questions in quizzes_data.items():
            print(f"\nProcessing quiz: '{quiz_name}'...")
            try:
                # **IMPROVEMENT**: Dynamically assign category instead of hardcoding
                category = get_category_for_quiz(quiz_name)
                
                db.add_quiz(quiz_name, category)
                print(f"-> Quiz '{quiz_name}' added to the database under '{category}'.")
                
                # Fetch the newly created quiz's ID to associate questions with it
                all_quizzes = db.get_all_quizzes()
                quiz_id = next((q['id'] for q in all_quizzes if q['name'] == quiz_name), None)

                if quiz_id and questions:
                    # Check if questions already exist for this quiz to avoid duplication
                    existing_questions = db.get_questions_for_quiz(quiz_id)
                    if not existing_questions:
                        for q in questions:
                            db.add_question(
                                quiz_id=quiz_id,
                                question_text=q['question'],
                                options=q['options'],
                                correct_option=q['correct_option'],
                                explanation=q.get('explanation', '') # Use .get for safety
                            )
                        print(f"-> Successfully loaded {len(questions)} questions for '{quiz_name}'.")
                    else:
                        print(f"-> Questions for '{quiz_name}' already exist. Skipping question loading.")
            except Exception as e:
                print(f"-> Quiz '{quiz_name}' likely already exists or an error occurred. Skipping. Error: {e}")
    else:
        print(f"WARNING: '{QUESTIONS_JSON_FILE}' not found. Skipping quiz loading.")

    # --- Load Full Syllabus from Pre-defined Structure (No changes needed here) ---
    print("\n--- Loading Full Syllabus ---")
    
    syllabus_structure = {
        "SAP": {
            "SAP Security & GRC": [
                {"title": "Module 1: S/4 HANA Introduction", "lessons": ["Versions of S/4 HANA", "Difference between S/4 HANA and HANA DB", "Architecture of S/4 HANA"]},
                {"title": "Module 2: Introduction to Security", "lessons": ["Importance of Security", "Overview of Network, Database, OS & Application Level Security", "Security standards & framework"]},
                {"title": "Module 3: User Maintenance", "lessons": ["User master record & objects", "User types", "Create new user account", "Mass user maintenance", "Associated tables", "Relevant Reports"]},
                {"title": "Module 4: Role Management", "lessons": ["Authorization Structure", "Profiles vs Roles", "Creation, Changes, Deletion of Roles", "Role Comparison", "Associated tables", "Relevant Reports"]},
                {"title": "Module 5: Fiori Security (ADM 945)", "lessons": ["Fiori Introduction & Architecture", "Fiori Apps, Catalogs, Groups, Spaces & Pages", "Fiori Role Design (PFCG)", "Troubleshooting Fiori issues"]},
                {"title": "Module 6: Security Parameter Configuration & Maintenance", "lessons": ["Checking Parameters", "Updating parameter", "Explaining various parameter & policies"]},
                {"title": "Module 7: Reporting Tools", "lessons": ["SUIM Reporting", "Reporting from Security Tables", "SQVI Reporting"]},
                {"title": "Module 8: Audit", "lessons": ["Configuring and running Audit", "Checking Logs Course Curriculum"]},
                {"title": "Module 9: Upgrade Activities", "lessons": ["Upgrades activities listing", "Updating Role", "Deprecated Transactions"]},
                {"title": "Module 10: SAP GRC - Access Risk Management", "lessons": ["Configuration", "Global SOD Matrix", "Risk ID Setup & Simulation", "Ruleset Maintenance & Transport", "Reporting"]},
                {"title": "Module 11: SAP GRC - Access Request Management", "lessons": ["Activation of workflow", "MSMP Workflows & BRF+", "Provisioning settings", "Customization of Access Request Management"]},
                {"title": "Module 12: SAP GRC - Business Role Management", "lessons": ["Define role naming conventions", "Workflow for Role Maintenance", "Single, Master, and Composite Role Creation", "Role Upload & Reports"]},
                {"title": "Module 13: SAP GRC - Emergency Access Management", "lessons": ["Centralized & Decentralized FFID Models", "Workflow for Super User Access", "Configure Log Reports", "EAM Reports Monitoring"]},
                {"title": "Module 14: S/4 HANA Public Cloud Security", "lessons": ["User Role Management Apps", "Transport Concepts (ATO & BCP)", "Cloud Identity Service (IAS)", "User Access Review (UAR)"]}
            ],
            "SAP SuccessFactors Employee Central": [
                {"title": "Module 1: Introduction to Cloud & SuccessFactors", "lessons": ["Introduction to Cloud Solutions", "Why SuccessFactors", "On-Premise Vs Cloud", "Implementation Methodologies", "SuccessFactors System Architecture"]},
                {"title": "Module 2: Initial System Setup", "lessons": ["Super Admin Creation", "Role-Based Permission Access", "Home Page Setup", "Admin Center Tools", "Theme Manager"]},
                {"title": "Module 3: Employee Central Core", "lessons": ["EC Implementation Steps", "Data Models Overview (XML)", "Foundation Objects", "MDF Objects", "Personal and Employment Objects"]},
                {"title": "Module 4: Data Management & Associations", "lessons": ["Import and Export Data", "Foundation Object Imports", "Object Associations", "Picklist Center", "Business Configuration UI"]},
                {"title": "Module 5: Business Rules & Workflows", "lessons": ["Business Rules Configuration (Object, Portlet, Field)", "Workflow Rules", "Workflow Roles (Dynamic Role, Dynamic Group)", "Events and Event Reasons"]},
                {"title": "Module 6: Permissions & Position Management", "lessons": ["Manage Permissions Roles & Groups", "User Permissions", "Global Assignment", "Position Management", "Data Migration", "HRIS Sync Job"]},
                {"title": "Module 7 & 8: Live Project Workshop", "lessons": ["End-to-end implementation workshop"]},
                {"title": "Module 9 & 10: Career Prep", "lessons": ["Resume Preparation", "LinkedIn Profile Building"]},
                {"title": "Module 11 & 12: Interview Preparation", "lessons": ["Mock Interviews (Functional, Technical, Project)"]}
            ]
        },
        "Generative AI": {
            "GenAI & Agentic AI": [
                {"title": "Topic 1: Python", "lessons": ["Basics of Python", "Control Flow and Loops", "Data Structures", "Functions and Modules", "File Handling and Exceptions", "Object-Oriented Programming (OOP)"]},
                {"title": "Topic 2: Machine Learning Fundamentals", "lessons": ["Introduction to Machine Learning", "Classification and Regression Algorithms", "Overfitting and Regularization", "Introduction to Neural Networks"]},
                {"title": "Topic 3: Deep Learning Basics", "lessons": ["Introduction to Deep Learning", "Optimization in Deep Learning", "Introduction to NLP", "Recurrent Neural Networks (RNN)"]},
                {"title": "Topic 4: Mastering Embeddings, LSTMs, Transformers and Gen AI", "lessons": ["Introduction to Vector Embeddings", "LSTMs – Architecture & Implementation", "Advanced LSTM Concepts & Transition to Transformers", "Gen AI Essentials", "Prompt Engineering"]},
                {"title": "Topic 5: Mastering LangChain, LangGraph & LangFlow", "lessons": ["Introduction to LangChain & Its Core Framework", "Building and Integrating LLM Applications", "LangChain Chains & Their Specialties", "Graph-Based AI Workflows with LangGraph", "Scaling, Optimizing & Deploying AI Applications"]},
                {"title": "Topic 6: Retrieval-Augmented Generation (RAG)", "lessons": ["Introduction to RAG", "Architecture of RAG", "Implementing RAG with Hugging Face", "Applications: Open-domain Q&A", "Advanced topics: Fine-tuning RAG"]},
                {"title": "Topic 7: Agents and Agentic RAG (using LangGraph)", "lessons": ["Introduction to Agents", "Agentic frameworks", "Combining RAG with agents", "Implementing an Agentic RAG system"]},
                {"title": "Topic 8: Introduction to MCP (Model Context Protocol)", "lessons": ["MCP Architecture and Core Components", "MCP Environment Setup", "MCP Hands-on"]},
                {"title": "Capstone Project", "lessons": ["Building an AI-powered Multi-Agent Q&A system"]}
            ]
        }
    }

    # This part of the script remains effective and does not require changes.
    for category_name, courses in syllabus_structure.items():
        print(f"\nProcessing syllabus category: '{category_name}'...")
        try:
            db.add_syllabus_category(category_name)
            cat_id = next((c['id'] for c in db.get_syllabus_categories() if c['name'] == category_name), None)
            
            if cat_id:
                for course_name, modules in courses.items():
                    db.add_syllabus_course(course_name, cat_id)
                    course_id = next((c['id'] for c in db.get_syllabus_courses(cat_id) if c['name'] == course_name), None)
                    
                    if course_id:
                        for module_data in modules:
                            db.add_syllabus_module(module_data['title'], course_id)
                            module_id = next((m['id'] for m in db.get_syllabus_modules(course_id) if m['title'] == module_data['title']), None)
                            
                            if module_id:
                                for lesson_title in module_data['lessons']:
                                    db.add_syllabus_lesson(lesson_title, "Lesson", module_id)
                print(f"-> Successfully loaded syllabus for '{category_name}'.")
        except Exception:
            print(f"-> Syllabus category '{category_name}' likely already exists. Skipping.")

    print("\n\nData loading complete!")

if __name__ == '__main__':
    load_initial_data()