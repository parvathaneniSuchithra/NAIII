import streamlit as st
import pandas as pd
import json
import database as db
import plotly.express as px
import time
import os
from datetime import datetime

# --- Custom CSS for a beautiful and themed interface ---
def apply_custom_css(theme):
    """Applies custom CSS to the Streamlit app, with support for light and dark themes."""
    light_theme_vars = """
        --primary-color: #4A90E2; /* Softer professional blue */
        --secondary-color: #6C757D; /* Muted grey */
        --background-color: #F8F9FA; /* Light grey background */
        --card-background: #FFFFFF; /* White cards */
        --text-color: #343A40; /* Dark charcoal text */
        --border-color: #DEE2E6; /* Light grey border */
        --shadow: rgba(0, 0, 0, 0.08) 0px 4px 12px; /* Subtle shadow */
        --accent-color: #28A745; /* Green for success */
        --font-size-base: 16px; /* Increased base font size */
        --font-size-large: 24px; /* Larger font for headers */
        --font-size-medium: 18px; /* Medium font for subheadings */
    """

    dark_theme_vars = """
        --primary-color: #7DB9EE; /* Brighter blue for dark theme */
        --secondary-color: #ADB5BD; /* Lighter grey text */
        --background-color: #212529; /* Dark charcoal background */
        --card-background: #2C3034; /* Dark grey cards */
        --text-color: #E9ECEF; /* Off-white text */
        --border-color: #495057; /* Medium dark border */
        --shadow: rgba(0, 0, 0, 0.4) 0px 4px 12px; /* Pronounced shadow */
        --accent-color: #28A745; /* Green for success */
        --font-size-base: 16px; /* Increased base font size */
        --font-size-large: 24px; /* Larger font for headers */
        --font-size-medium: 18px; /* Medium font for subheadings */
    """
    
    css = f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Poppins:wght@600;700&display=swap');

            :root {{
                {light_theme_vars if theme == "light" else dark_theme_vars}
                --border-radius: 0.75rem;
            }}

            body {{
                font-family: 'Inter', sans-serif;
                font-size: var(--font-size-base);
            }}

            .stApp {{
                background-color: var(--background-color);
                color: var(--text-color);
            }}

            .main .block-container {{
                padding: 1.5rem 2rem;
                max-width: 1200px;
                margin: 0 auto;
            }}

            h1, h2, h3 {{
                font-family: 'Poppins', sans-serif;
                color: var(--primary-color);
            }}
            
            h1 {{ font-size: var(--font-size-large); }}
            h2 {{ font-size: var(--font-size-large); }}
            h3 {{ font-size: var(--font-size-medium); }}

            .brand-header {{
                font-family: 'Poppins', sans-serif;
                font-size: var(--font-size-large);
                font-weight: 700;
                color: var(--primary-color);
                text-align: center;
                margin-bottom: 1rem;
            }}

            .brand-subtitle {{
                font-size: var(--font-size-medium);
                font-weight: 400;
                color: var(--secondary-color);
                text-align: center;
                margin-top: 0;
                margin-bottom: 2rem;
            }}

            .stButton > button {{
                width: 100%;
                border: none;
                text-align: left;
                padding: 1rem 1.5rem;
                margin-bottom: 1rem;
                border-radius: var(--border-radius);
                font-weight: 500;
                font-size: var(--font-size-base);
                background-color: var(--primary-color);
                color: var(--card-background);
                box-shadow: var(--shadow);
                transition: all 0.2s ease-in-out;
                cursor: pointer;
            }}

            .stButton > button:hover {{
                filter: brightness(1.1);
                transform: scale(1.02);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            }}

            .stButton > button:disabled {{
                background-color: var(--secondary-color);
                color: #E9ECEF;
                cursor: not-allowed;
            }}

            div[data-testid="stButton-logout_btn"] > button {{
                background-color: var(--secondary-color);
            }}

            div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {{
                background-color: var(--card-background);
                padding: 2rem;
                border-radius: var(--border-radius);
                box-shadow: var(--shadow);
                margin-bottom: 2rem;
            }}

            [data-tooltip] {{
                position: relative;
                cursor: pointer;
            }}
            [data-tooltip]:hover:after {{
                content: attr(data-tooltip);
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: var(--card-background);
                color: var(--text-color);
                padding: 0.75rem;
                border-radius: 0.25rem;
                font-size: var(--font-size-base);
                white-space: nowrap;
                z-index: 1000;
                box-shadow: var(--shadow);
            }}

            @media (max-width: 768px) {{
                .main .block-container {{
                    padding: 1rem;
                }}
                .stButton > button {{
                    font-size: var(--font-size-base);
                    padding: 0.75rem 1rem;
                }}
                h1, h2, h3 {{
                    font-size: var(--font-size-medium);
                }}
            }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- Session State Management ---
def initialize_session_state():
    """Initializes all necessary session state variables."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "user_category" not in st.session_state:
        st.session_state.user_category = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    if "remember_me" not in st.session_state:
        st.session_state.remember_me = False

    # Quiz-specific state
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "current_quiz_id" not in st.session_state:
        st.session_state.current_quiz_id = None
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "student_answers" not in st.session_state:
        st.session_state.student_answers = []
    if "show_explanation" not in st.session_state:
        st.session_state.show_explanation = False
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False
    if "selection" not in st.session_state:
        st.session_state.selection = None
    if "last_answer_correct" not in st.session_state:
        st.session_state.last_answer_correct = False
    if "quiz_time_left" not in st.session_state:
        st.session_state.quiz_time_left = 30

def reset_quiz_state():
    """Resets all quiz-related session state variables."""
    st.session_state.quiz_started = False
    st.session_state.current_quiz_id = None
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.student_answers = []
    st.session_state.show_explanation = False
    st.session_state.quiz_completed = False
    st.session_state.selection = None
    st.session_state.quiz_time_left = 30

# --- UI Components ---
def display_logo():
    st.markdown("<div class='brand-header'>NeuroverseAI</div>", unsafe_allow_html=True)
    st.markdown("<p class='brand-subtitle'>GenAI & SAP Training</p>", unsafe_allow_html=True)

def display_progress_bar(current, total):
    """Displays a progress bar for quizzes or syllabus."""
    if total > 0:
        progress = current / total
        st.progress(progress, text=f"Progress: {current}/{total}")

# --- Page Renderers ---
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            display_logo()
            st.header("Login")
            with st.form("login_form"):
                username = st.text_input("Username", value=st.session_state.get("username", "") if st.session_state.remember_me else "")
                password = st.text_input("Password", type="password", value=st.session_state.get("password", "") if st.session_state.remember_me else "")
                remember_me = st.checkbox("Remember Me", value=st.session_state.remember_me)
                submitted = st.form_submit_button("Login")
                if submitted:
                    if not username or not password:
                        st.error("Username and password are required.")
                    else:
                        user = db.get_user(username)
                        if user and user["password"] == password:
                            st.session_state.logged_in = True
                            st.session_state.username = user["username"]
                            st.session_state.user_role = user["role"]
                            st.session_state.user_id = user["id"]
                            st.session_state.user_category = user["category"]
                            st.session_state.current_page = "Home"
                            st.session_state.remember_me = remember_me
                            if remember_me:
                                st.session_state.username = username
                                st.session_state.password = password
                            st.success("Logged in successfully!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")

def home_page():
    st.title(f"Welcome, {st.session_state.username}!")
    progress = db.get_user_progress(st.session_state.user_id)
    total_quizzes = len(progress) if progress else 0
    avg_score = sum(p["score"] for p in progress) / total_quizzes if total_quizzes > 0 else 0
    motivation = "Keep up the great work!" if avg_score > 70 else "You're on your way—keep learning!"
    st.write(f"**Quick Stats**: Quizzes Attempted: {total_quizzes}, Average Score: {avg_score:.1f}%")
    st.success(motivation)
    st.write("Navigate using the sidebar to take a quiz, view your scores, or explore the syllabus.")

def view_syllabus_page():

    search_term = st.text_input("Search Courses, Modules, or Lessons")
    
    categories = db.get_syllabus_categories()

    if not categories:
        st.info("The syllabus is currently empty. Please contact an administrator.")
        return

    for category in categories:
        with st.container():
            st.subheader(category['name'])
            courses = db.get_syllabus_courses(category['id'])
            if not courses:
                st.write(f"*No courses available in {category['name']}.*")
                continue
            for course in courses:
                if search_term.lower() in course['name'].lower():
                    with st.expander(course['name'], expanded=False):
                        modules = db.get_syllabus_modules(category['id'], course['id'])
                        if not modules:
                            st.write("*No modules available in this course.*")
                            continue
                        for module in modules:
                            if search_term.lower() in module['title'].lower():
                                st.markdown(f"**{module['title']}**")
                                lessons = db.get_syllabus_lessons(category['id'], course['id'], module['id'])
                                if lessons:
                                    for lesson in lessons:
                                        if search_term.lower() in lesson['title'].lower():
                                            st.markdown(f"- {lesson['title']} (*{lesson['type']}*)")
                                else:
                                    st.markdown("  - *No lessons in this module.*")
                                st.markdown("---")

def student_quiz_page():
    if not st.session_state.quiz_started:
        st.title(f"Quizzes for {st.session_state.user_category}")
        available_quizzes = db.get_quizzes_by_category(st.session_state.user_category)
        if not available_quizzes:
            st.warning(f"No quizzes are currently available for your assigned category: '{st.session_state.user_category}'.")
            return
        
        quiz_options = {quiz['name']: quiz['id'] for quiz in available_quizzes}
        selected_quiz_name = st.selectbox("Choose a quiz to start:", list(quiz_options.keys()))
        if st.button("Start Quiz", key="start_quiz", help="Begin the selected quiz"):
            st.session_state.current_quiz_id = quiz_options[selected_quiz_name]
            st.session_state.quiz_started = True
            st.session_state.quiz_time_left = 30
            st.rerun()
    else:
        display_quiz()
def display_quiz():
    quiz_id = st.session_state.current_quiz_id
    questions = db.get_questions_for_quiz(quiz_id)
    total_questions = len(questions)
    
    if st.session_state.quiz_completed:
        display_quiz_dashboard(total_questions)
        return

    q_index = st.session_state.current_question_index
    if q_index >= total_questions:
        st.session_state.quiz_completed = True
        db.save_user_progress(st.session_state.user_id, quiz_id, st.session_state.score, total_questions, True, st.session_state.student_answers)
        st.rerun()

    current_question = questions[q_index]
    options = json.loads(current_question["options"])
    
    try:
        correct_answers = json.loads(current_question["correct_option"])
        is_multi_answer = isinstance(correct_answers, list)
    except (json.JSONDecodeError, TypeError):
        correct_answers = current_question["correct_option"]
        is_multi_answer = False

    st.title("Quiz in Progress")
    display_progress_bar(q_index + 1, total_questions)
    
    st.markdown("<div class='quiz-container'>", unsafe_allow_html=True)
    
    st.subheader(f"Question {q_index + 1}:")
    st.markdown(f"<h4>{current_question['question_text']}</h4>", unsafe_allow_html=True)
    is_submitted = st.session_state.show_explanation

    if is_multi_answer:
        st.info("This question may have multiple correct answers.")
        
        selections = []
        for option in options:
            if st.checkbox(option, key=f"q_{q_index}_opt_{option}", disabled=is_submitted):
                selections.append(option)
        st.session_state.selection = selections

    else:
        default_index = None
        if st.session_state.get('selection') in options:
            default_index = options.index(st.session_state.selection)
        
        st.session_state.selection = st.radio(
            "Select one answer:", options, 
            key=f"q_radio_{q_index}",
            index=default_index,
            disabled=is_submitted
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

    action_col, feedback_col = st.columns([1, 4])

    with action_col:
        if is_submitted:
            if st.button("Next", key="next_q", type="primary", use_container_width=True):
                st.session_state.current_question_index += 1
                st.session_state.show_explanation = False
                st.session_state.selection = None
                st.rerun()
        else:
            if st.button("Submit", disabled=not st.session_state.get('selection'), use_container_width=True):
                selection = st.session_state.selection
                is_correct = (set(selection) == set(correct_answers)) if is_multi_answer else (selection == correct_answers)
                
                if is_correct:
                    st.session_state.score += 1
                
                st.session_state.student_answers.append({
                    "question": current_question["question_text"],
                    "selected": selection,
                    "correct": correct_answers,
                    "is_correct": is_correct
                })
                st.session_state.last_answer_correct = is_correct
                st.session_state.show_explanation = True
                st.rerun()

    with feedback_col:
        if is_submitted:
            is_correct = st.session_state.last_answer_correct
            feedback_icon = "✅ Correct!" if is_correct else "❌ Incorrect"
            border_color = "var(--accent-color)" if is_correct else "#dc3545"
            
            correct_display = ", ".join(correct_answers) if is_multi_answer else correct_answers
            
            # Use a container with a bordered box for feedback
            with st.container():
                with st.expander(f"{feedback_icon}", expanded=True):
                    if not is_correct:
                        st.write(f"Correct Answer(s): {correct_display}")
                    st.write(f"Explanation: {current_question['explanation']}")
def display_quiz_dashboard(total_questions):
    st.header("🎉 Quiz Completed! 🎉")
    with st.container():
        score = st.session_state.score
        accuracy = (score / total_questions * 100) if total_questions > 0 else 0
        
        col1, col2 = st.columns(2)
        col1.metric("Your Score", f"{score}/{total_questions}")
        col2.metric("Accuracy", f"{accuracy:.1f}%")
        
        st.subheader("Review Your Answers")
        for i, answer in enumerate(st.session_state.student_answers):
            with st.container():
                st.markdown(f"**Q{i+1}: {answer['question']}**")
                status = "✅ Correct" if answer["is_correct"] else "❌ Incorrect"
                
                selected_display = ", ".join(answer['selected']) if isinstance(answer['selected'], list) else answer['selected']
                correct_display = ", ".join(answer['correct']) if isinstance(answer['correct'], list) else answer['correct']
                
                st.write(f"Your answer: `{selected_display}` ({status})")
                if not answer["is_correct"]:
                    st.write(f"Correct answer(s): `{correct_display}`")
                st.markdown("---")
            
    if st.button("Take Another Quiz", help="Start a new quiz"):
        reset_quiz_state()
        st.rerun()
    
    answers_json = json.dumps(st.session_state.student_answers, indent=4)
    st.download_button(
        label="Export Scores", 
        data=answers_json, 
        file_name="quiz_results.json", 
        mime="application/json", 
        help="Download your quiz results"
    )

def view_my_scores_page():
    st.title("My Scores")
    
    progress_records = db.get_user_progress(st.session_state.user_id)
    
    if not progress_records:
        st.info("You have not completed any quizzes yet.")
        return

    df_data = []
    for record in reversed(progress_records):
        ts = record['timestamp'] if 'timestamp' in record else None
        
        date_str_for_df = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S') if ts else "N/A"
        df_data.append({
            "Quiz Name": record['quiz_name'],
            "Score": record['score'],
            "Total": record['total'],
            "Date": date_str_for_df
        })

        date_str_for_expander = f"on {datetime.fromtimestamp(ts).strftime('%Y-%m-%d')}" if ts else ""
        expander_title = f"Quiz: {record['quiz_name']} - Score: {record['score']}/{record['total']} {date_str_for_expander}"
        
        with st.expander(expander_title):
            try:
                answers = json.loads(record['answers_log'])
                for i, answer in enumerate(answers):
                    st.markdown(f"**Q{i+1}: {answer['question']}**")
                    status = "✅" if answer["is_correct"] else "❌"

                    selected_display = ", ".join(answer['selected']) if isinstance(answer['selected'], list) else answer['selected']
                    correct_display = ", ".join(answer['correct']) if isinstance(answer['correct'], list) else answer['correct']

                    st.write(f"Your answer: {selected_display} {status}")
                    if not answer["is_correct"]:
                        st.write(f"Correct answer(s): {correct_display}")
                    st.markdown("---")
            except (json.JSONDecodeError, TypeError):
                st.warning("Could not load answer details for this quiz attempt.")

    scores_df = pd.DataFrame(df_data)
    
    plot_df = scores_df[scores_df["Date"] != "N/A"].copy()

    if not plot_df.empty:
        st.subheader("Score Trend Over Time")
        plot_df['Date'] = pd.to_datetime(plot_df['Date'])
        
        # 1. Create a new column for the accuracy percentage
        plot_df['Accuracy (%)'] = (plot_df['Score'] / plot_df['Total'] * 100).round(2)

        # 2. Tell the chart to use the new 'Accuracy (%)' column
        fig = px.line(
            plot_df.sort_values(by='Date'), 
            x="Date", 
            y="Accuracy (%)", 
            title="Your Score History", 
            markers=True
        )
        # 3. Update the y-axis title to match
        fig.update_layout(xaxis_title="Date of Attempt", yaxis_title="Accuracy (%)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No scores with timestamps are available to plot a trend.")

# --- Admin Panel ---
def admin_page():
    st.sidebar.title("Admin Panel")
    
    if "admin_sub_page" not in st.session_state:
        st.session_state.admin_sub_page = "Manage Categories"

    admin_options = {
        "Manage Categories": "Manage user and quiz categories",
        "Manage Syllabus": "Manage syllabus structure",
        "Manage Quizzes": "Manage quizzes and questions",
        "Manage Users": "Manage user accounts",
        "View Performance": "View trainee performance"
    }
    
    for page, tooltip in admin_options.items():
        if st.sidebar.button(page, key=f"nav_admin_{page.lower().replace(' ', '_')}", help=tooltip):
            st.session_state.admin_sub_page = page
            st.rerun()

    sub_page = st.session_state.admin_sub_page
    
    if sub_page == "Manage Categories":
        manage_categories_section()
    elif sub_page == "Manage Syllabus":
        manage_syllabus_section()
    elif sub_page == "Manage Quizzes":
        manage_quizzes_section()
    elif sub_page == "Manage Users":
        manage_users_section()
    elif sub_page == "View Performance":
        view_trainee_performance_section()
    else: 
        manage_categories_section()

def manage_categories_section():
    st.header("Manage User & Quiz Categories")
    
    with st.container():
        with st.form("create_category_form", clear_on_submit=True):
            st.subheader("Create New Category")
            category_name = st.text_input("New Category Name")
            if st.form_submit_button("Create Category", help="Add a new category"):
                if not category_name:
                    st.error("Category name cannot be empty.")
                else:
                    try:
                        db.add_category(category_name)
                        st.success(f"Category '{category_name}' created.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not create category. It might already exist. Error: {e}")

    with st.container():
        st.subheader("Existing Categories")
        search_term = st.text_input("Search Categories")
        categories = [c for c in db.get_categories() if search_term.lower() in c['name'].lower()]
        if not categories:
            st.info("No categories found.")
            return
            
        for category in categories:
            with st.expander(f"Edit Category: {category['name']}"):
                with st.form(key=f"edit_cat_{category['id']}"):
                    new_name = st.text_input("Category Name", value=category['name'])
                    col1, col2 = st.columns([1, 1])
                    if col1.form_submit_button("Save Changes", help="Update category name"):
                        if not new_name:
                            st.error("Category name cannot be empty.")
                        else:
                            db.update_category(category['id'], new_name)
                            st.success("Category updated.")
                            st.rerun()
                    if col2.form_submit_button("Delete", type="secondary", help="Delete this category"):
                        try:
                            db.delete_category(category['id'])
                            st.warning("Category deleted.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Could not delete category. It may be in use. Error: {e}")

def manage_syllabus_section():
    st.header("Manage Syllabus")

    with st.expander("Manage Syllabus Categories", expanded=True):
        st.subheader("Create New Syllabus Category")
        with st.form("new_syllabus_cat", clear_on_submit=True):
            new_cat_name = st.text_input("Category Name")
            if st.form_submit_button("Create"):
                db.add_syllabus_category(new_cat_name)
                st.success(f"Syllabus category '{new_cat_name}' created.")
                st.rerun()

        st.subheader("Existing Syllabus Categories")
        for cat in db.get_syllabus_categories():
            with st.form(key=f"edit_syl_cat_{cat['id']}"):
                new_name = st.text_input("Name", value=cat['name'])
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Update"):
                    db.update_syllabus_category(cat['id'], new_name)
                    st.success("Updated.")
                    st.rerun()
                if c2.form_submit_button("Delete"):
                    db.delete_syllabus_category(cat['id'])
                    st.warning("Deleted.")
                    st.rerun()

    all_syl_cats = db.get_syllabus_categories()
    if not all_syl_cats:
        st.info("Create a syllabus category to add courses.")
        return

    cat_options = {c['name']: c['id'] for c in all_syl_cats}
    selected_cat_name = st.selectbox("Select Syllabus Category to Manage", options=list(cat_options.keys()))
    selected_cat_id = cat_options[selected_cat_name]

    with st.expander("Manage Courses", expanded=True):
        st.subheader(f"Create New Course in '{selected_cat_name}'")
        with st.form("new_course", clear_on_submit=True):
            course_name = st.text_input("Course Name")
            if st.form_submit_button("Create Course"):
                db.add_syllabus_course(course_name, selected_cat_id)
                st.success(f"Course '{course_name}' created.")
                st.rerun()
        
        st.subheader("Existing Courses")
        for course in db.get_syllabus_courses(selected_cat_id):
            with st.container():
                st.write(f"**Course: {course['name']}**")
                with st.expander("Manage Modules & Lessons"):
                    st.markdown("---")
                    st.write("**Modules**")
                    for module in db.get_syllabus_modules(course['id']):
                        st.write(f"- {module['title']}")
                    with st.form(f"new_module_{course['id']}", clear_on_submit=True):
                        module_title = st.text_input("New Module Title")
                        if st.form_submit_button("Add Module"):
                            db.add_syllabus_module(module_title, course['id'])
                            st.rerun()

                    st.markdown("---")
                    st.write("**Lessons**")
                    modules_for_course = db.get_syllabus_modules(course['id'])
                    if modules_for_course:
                        module_options = {m['title']: m['id'] for m in modules_for_course}
                        selected_module_title = st.selectbox("Select Module to Add Lesson", options=list(module_options.keys()), key=f"mod_select_{course['id']}")
                        selected_module_id = module_options[selected_module_title]
                        
                        for lesson in db.get_syllabus_lessons(selected_module_id):
                            st.write(f"  - {lesson['title']} ({lesson['type']})")

                        with st.form(f"new_lesson_{selected_module_id}", clear_on_submit=True):
                            lesson_title = st.text_input("New Lesson Title")
                            lesson_type = st.selectbox("Lesson Type", ["Lesson", "Video", "Reading"])
                            if st.form_submit_button("Add Lesson"):
                                db.add_syllabus_lesson(lesson_title, lesson_type, selected_module_id)
                                st.rerun()
                st.markdown("---")

def manage_quizzes_section():
    st.header("Manage Quizzes and Questions")

    with st.expander("Create New Quiz", expanded=True):
        with st.form("new_quiz_form", clear_on_submit=True):
            quiz_name = st.text_input("Quiz Name")
            categories = db.get_categories()
            cat_options = [c['name'] for c in categories] if categories else []
            quiz_category = st.selectbox("Category", cat_options)
            if st.form_submit_button("Create Quiz"):
                if quiz_name and quiz_category:
                    db.add_quiz(quiz_name, quiz_category)
                    st.success(f"Quiz '{quiz_name}' created in category '{quiz_category}'.")
                    st.rerun()
                else:
                    st.error("Quiz name and category are required.")

    st.markdown("---")
    
    all_quizzes = db.get_all_quizzes()
    if not all_quizzes:
        st.info("No quizzes exist. Create a quiz to add questions.")
        return

    quiz_options = {f"{q['name']} ({q['category']})": q['id'] for q in all_quizzes}
    selected_quiz_label = st.selectbox("Select a quiz to manage", list(quiz_options.keys()), key="quiz_selector")
    selected_quiz_id = quiz_options[selected_quiz_label]

    st.subheader(f"Add New Question to '{selected_quiz_label}'")
    
    option_1 = st.text_input("Option 1", key="opt1")
    option_2 = st.text_input("Option 2", key="opt2")
    option_3 = st.text_input("Option 3", key="opt3")
    option_4 = st.text_input("Option 4", key="opt4")
    
    question_type = st.radio("Question Type", ("Single Answer", "Multiple Answers"), horizontal=True, key="q_type")
    
    with st.form(f"add_question_form_{selected_quiz_id}", clear_on_submit=True):
        question_text = st.text_area("Question Text")
        st.markdown("---")

        defined_options = [opt.strip() for opt in [option_1, option_2, option_3, option_4] if opt.strip()]

        correct_answer = None
        if not defined_options:
            st.warning("Enter text in the option boxes above to select a correct answer.")
        else:
            if question_type == "Single Answer":
                correct_answer = st.selectbox("Correct Option", options=["Select an option"] + defined_options)
            else:
                correct_answer = st.multiselect("Correct Options", options=defined_options)

        explanation = st.text_area("Explanation")
        
        submitted = st.form_submit_button("Add Question to Quiz", type="primary", use_container_width=True)
        if submitted:
            final_options = [opt.strip() for opt in [st.session_state.opt1, st.session_state.opt2, st.session_state.opt3, st.session_state.opt4] if opt.strip()]

            # --- FIX: Convert list to JSON string for the database ---
            final_correct_answer = correct_answer
            if isinstance(correct_answer, list):
                final_correct_answer = json.dumps(correct_answer)

            if not question_text:
                st.error("Question text cannot be empty.")
            elif len(final_options) < 2:
                st.error("You must provide at least two non-empty options.")
            elif not correct_answer or correct_answer == "Select an option":
                st.error("You must select a correct answer.")
            elif not explanation:
                st.error("Please provide an explanation.")
            else:
                # The database function in the traceback expects a string, not a list
                db.add_question(selected_quiz_id, question_text, final_options, final_correct_answer, explanation)
                st.success("Question added successfully!")
    
    st.markdown("---")
    st.subheader("Edit Existing Questions")
    
    questions = db.get_questions_for_quiz(selected_quiz_id)
    if not questions:
        st.info("This quiz has no questions yet.")
    else:
        for q in questions:
            with st.expander(f"Edit: {q['question_text'][:50]}..."):
                with st.form(key=f"edit_q_{q['id']}"):
                    new_text = st.text_area("Question", value=q['question_text'], key=f"text_{q['id']}")
                    current_options = json.loads(q['options'])
                    new_options_text = st.text_area("Options (one per line)", value="\n".join(current_options), key=f"opts_{q['id']}")
                    new_explanation = st.text_area("Explanation", value=q['explanation'], key=f"exp_{q['id']}")

                    is_currently_multi = False
                    correct_answers_value = q['correct_option']
                    try:
                        parsed_correct = json.loads(q['correct_option'])
                        if isinstance(parsed_correct, list):
                            is_currently_multi = True
                            correct_answers_value = parsed_correct
                    except (json.JSONDecodeError, TypeError):
                        pass

                    is_now_multi = st.checkbox("Question has multiple correct answers", value=is_currently_multi, key=f"is_multi_edit_{q['id']}")
                    
                    if is_now_multi:
                        display_values = "\n".join(correct_answers_value) if isinstance(correct_answers_value, list) else correct_answers_value
                        new_correct_text = st.text_area("Correct Options (one per line)", value=display_values, key=f"correct_multi_{q['id']}")
                    else:
                        display_value = correct_answers_value[0] if isinstance(correct_answers_value, list) else correct_answers_value
                        new_correct_input = st.text_input("Correct Option", value=display_value, key=f"correct_single_{q['id']}")
                    
                    c1, c2 = st.columns(2)
                    if c1.form_submit_button("Update Question"):
                        new_options = [opt.strip() for opt in new_options_text.split('\n') if opt.strip()]
                        final_correct_value = None

                        if is_now_multi:
                            final_correct_answers = [opt.strip() for opt in new_correct_text.split('\n') if opt.strip()]
                            if final_correct_answers and all(ans in new_options for ans in final_correct_answers):
                                final_correct_value = json.dumps(final_correct_answers)
                            else:
                                st.error("All correct options must exist in the options list.")
                        else:
                            if new_correct_input in new_options:
                                final_correct_value = new_correct_input
                            else:
                                st.error("The correct answer must be one of the options.")
                        
                        if final_correct_value is not None:
                            db.update_question(q['id'], new_text, new_options, final_correct_value, new_explanation)
                            st.success("Question updated.")
                            st.rerun()

                    if c2.form_submit_button("Delete Question"):
                        db.delete_question(q['id'])
                        st.warning("Question deleted.")
                        st.rerun()

def manage_users_section():
    st.header("Manage Users")

    with st.expander("Add New User", expanded=True):
        with st.form("new_user_form", clear_on_submit=True):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["student", "admin"])
            
            categories = db.get_categories()
            cat_options = [c['name'] for c in categories] if categories else []
            category = st.selectbox("Assign to Category", cat_options)
            
            if st.form_submit_button("Add User"):
                if username and password and role and category:
                    db.add_user(username, password, role, category)
                    st.success(f"User '{username}' created.")
                    st.rerun()
                else:
                    st.error("All fields are required.")

    st.subheader("Existing Users")
    users = db.get_all_users()
    categories = db.get_categories()
    cat_options = [c['name'] for c in categories] if categories else []

    for user in users:
        with st.expander(f"Edit User: {user['username']} (Role: {user['role']})"):
            with st.form(key=f"edit_user_{user['id']}"):
                new_username = st.text_input("Username", value=user['username'])
                
                try:
                    current_cat_index = cat_options.index(user['category'])
                except ValueError:
                    current_cat_index = 0

                new_category = st.selectbox("Category", cat_options, index=current_cat_index)
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("Update User"):
                    db.update_user(user['id'], new_username, new_category)
                    st.success("User updated.")
                    st.rerun()
                if c2.form_submit_button("Delete User"):
                    if user['id'] == st.session_state.user_id:
                        st.error("You cannot delete your own account.")
                    else:
                        db.delete_user(user['id'])
                        st.warning("User deleted.")
                        st.rerun()

def view_trainee_performance_section():
    st.header("Trainee Performance Dashboard")

    progress_data = db.get_all_user_progress()
    if not progress_data:
        st.info("No quiz performance data available yet.")
        return

    # The progress_data from the optimized function already contains the username and category
    df = pd.DataFrame(progress_data)

    # Check if the necessary columns exist before proceeding
    required_cols = ['score', 'total', 'category', 'username', 'quiz_name', 'timestamp']
    if not all(col in df.columns for col in required_cols):
        st.error("The user progress data is missing required columns. Please check your `database.py` file.")
        st.dataframe(df)
        return

    df['accuracy'] = df.apply(
        lambda row: (row['score'] / row['total'] * 100) if row.get('total', 0) > 0 else 0,
        axis=1
    ).round(2)
    
    st.sidebar.header("Filters")
    categories = sorted(df['category'].dropna().unique())
    selected_cat = st.sidebar.multiselect("Filter by Category", options=categories, default=list(categories))
    
    if selected_cat:
        filtered_df = df[df['category'].isin(selected_cat)]
    else:
        # If nothing is selected, show an empty dataframe
        filtered_df = df.iloc[0:0]

    st.subheader("Overall Performance")
    avg_accuracy = filtered_df['accuracy'].mean()
    total_attempts = len(filtered_df)
    
    col1, col2 = st.columns(2)
    col1.metric("Average Accuracy", f"{avg_accuracy:.2f}%" if not pd.isna(avg_accuracy) else "N/A")
    col2.metric("Total Quiz Attempts", total_attempts)

    st.subheader("Performance by Quiz")
    quiz_performance = filtered_df.groupby('quiz_name').agg(
        average_accuracy=('accuracy', 'mean'),
        attempts=('username', 'count')
    ).reset_index()
    st.dataframe(quiz_performance)

    st.subheader("Performance by Trainee")
    trainee_performance = filtered_df.groupby('username').agg(
        average_accuracy=('accuracy', 'mean'),
        quizzes_taken=('quiz_name', 'count')
    ).reset_index()
    st.dataframe(trainee_performance)

    st.subheader("Raw Data")
    # Prepare a user-friendly view of the raw data
    display_cols = ['username', 'quiz_name', 'category', 'score', 'total', 'accuracy', 'timestamp']
    df_display = filtered_df[[col for col in display_cols if col in filtered_df.columns]].copy()
    # Convert timestamp to a readable format
    df_display['timestamp'] = pd.to_datetime(df_display['timestamp'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')
    st.dataframe(df_display)


# --- Main Application Logic ---
def main():
    initialize_session_state()
    apply_custom_css(st.session_state.theme)

    if not st.session_state.logged_in:
        login_page()
        return

    if st.session_state.get("current_page") == "Admin" and st.session_state.user_role == "admin":
        st.sidebar.title(f"Welcome, {st.session_state.username}")
        st.sidebar.write(f"Role: {st.session_state.user_role}")
        if st.sidebar.button("← Back to Student View"):
            st.session_state.current_page = "Home"
            st.rerun()
        st.sidebar.markdown("---")
        admin_page()
    else:
        st.sidebar.title(f"Welcome, {st.session_state.username}")
        st.sidebar.write(f"Role: {st.session_state.user_role}")
        st.sidebar.markdown("---")

        student_pages = ["Home", "Syllabus", "Take Quiz", "My Scores"]
        st.sidebar.header("Navigation")
        for page in student_pages:
            if st.sidebar.button(page, key=f"nav_{page.lower().replace(' ', '_')}"):
                st.session_state.current_page = page
                if page != "Take Quiz":
                    reset_quiz_state()
                st.rerun()
        
        if st.session_state.user_role == "admin":
            st.sidebar.markdown("---")
            st.sidebar.header("Admin")
            if st.sidebar.button("Admin Panel", key="nav_admin", help="Access administrative tools"):
                st.session_state.current_page = "Admin"
                st.rerun()
        
        st.sidebar.markdown("---")
        if st.sidebar.button("Logout", key="logout_btn", help="Log out of your account"):
            for key in list(st.session_state.keys()):
                if key not in ['theme', 'remember_me', 'username', 'password']:
                    del st.session_state[key]
            st.session_state.logged_in = False
            st.rerun()
        
        page = st.session_state.get("current_page", "Home")
        if page == "Home":
            home_page()
        elif page == "Syllabus":
            view_syllabus_page()
        elif page == "Take Quiz":
            student_quiz_page()
        elif page == "My Scores":
            view_my_scores_page()
        else:
            home_page()

if __name__ == "__main__":
    main()
    