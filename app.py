import streamlit as st
import json
import pandas as pd
import time
import database as db  # Import the new database module

# --- Custom CSS for a Clean, Modern, and Professional Look with Theme Support ---
def apply_custom_css(theme):
    # Define CSS variables for both light and dark themes
    # These variables will be used throughout the CSS for consistent styling
    light_theme_vars = """
        --primary-color: #4A90E2; /* A softer, more professional blue */
        --secondary-color: #6C757D; /* Muted grey for secondary elements */
        --background-color: #F8F9FA; /* Very light grey for main background */
        --card-background: #FFFFFF; /* Pure white for cards/containers */
        --text-color: #343A40; /* Dark charcoal for primary text */
        --accent-light: #EBF5FF; /* Very light blue for subtle highlights */
        --border-color: #DEE2E6; /* Light grey border */
        --shadow: rgba(0, 0, 0, 0.08) 0px 4px 12px 0px; /* Softer, more subtle shadow */
        --hover-shadow: rgba(0, 0, 0, 0.12) 0px 6px 18px 0px; /* Slightly more pronounced on hover */
        --success-bg: #D4EDDA; --success-text: #155724; --success-border: #C3E6CB;
        --error-bg: #F8D7DA; --error-text: #721C24; --error-border: #F5C6CB;
        --info-bg: #D1ECF1; --info-text: #0C5460; --info-border: #BEE5EB;
    """

    dark_theme_vars = """
        --primary-color: #7DB9EE; /* A brighter, yet professional blue for dark theme */
        --secondary-color: #ADB5BD; /* Lighter grey for secondary text */
        --background-color: #212529; /* Darker charcoal for main background */
        --card-background: #2C3034; /* Slightly lighter dark grey for cards */
        --text-color: #E9ECEF; /* Off-white for readability */
        --accent-light: #3A4045; /* Darker muted grey for accents */
        --border-color: #495057; /* Medium dark grey border */
        --shadow: rgba(0, 0, 0, 0.4) 0px 4px 12px; /* More pronounced shadow for dark theme */
        --hover-shadow: rgba(0, 0, 0, 0.6) 0px 6px 18px;
        --success-bg: #284D31; --success-text: #C8E6C9; --success-border: #388E3C;
        --error-bg: #6B2E35; --error-text: #FFCDD2; --error-border: #D32F2F;
        --info-bg: #2A5A6A; --info-text: #BBDEFB; --info-border: #1976D2;
    """

<<<<<<< HEAD
    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Poppins:wght@400;600;700&display=swap');
            :root {{
                {"/* Light Theme */" if theme == "light" else "/* Dark Theme */"}
                {light_theme_vars if theme == "light" else dark_theme_vars}
                --border-radius: 0.75rem;
=======
# --- Custom CSS for a Clean, Modern, and Professional Professional Look with Theme Support ---
def apply_custom_css(theme):
    # Define CSS variables for both light and dark themes
    # These variables will be used throughout the CSS for consistent styling
    light_theme_vars = """
        --primary-color: #4A90E2; /* A softer, more professional blue */
        --secondary-color: #6C757D; /* Muted grey for secondary elements */
        --background-color: #F8F9FA; /* Very light grey for main background */
        --card-background: #FFFFFF; /* Pure white for cards/containers */
        --text-color: #343A40; /* Dark charcoal for primary text */
        --accent-light: #EBF5FF; /* Very light blue for subtle highlights */
        --border-color: #DEE2E6; /* Light grey border */
        --shadow: rgba(0, 0, 0, 0.08) 0px 4px 12px 0px; /* Softer, more subtle shadow */
        --hover-shadow: rgba(0, 0, 0, 0.12) 0px 6px 18px 0px; /* Slightly more pronounced on hover */
        --success-bg: #D4EDDA; --success-text: #155724; --success-border: #C3E6CB;
        --error-bg: #F8D7DA; --error-text: #721C24; --error-border: #F5C6CB;
        --info-bg: #D1ECF1; --info-text: #0C5460; --info-border: #BEE5EB;
    """

    dark_theme_vars = """
        --primary-color: #7DB9EE; /* A brighter, yet professional blue for dark theme */
        --secondary-color: #ADB5BD; /* Lighter grey for secondary text */
        --background-color: #212529; /* Darker charcoal for main background */
        --card-background: #2C3034; /* Slightly lighter dark grey for cards */
        --text-color: #E9ECEF; /* Off-white for readability */
        --accent-light: #3A4045; /* Darker muted grey for accents */
        --border-color: #495057; /* Medium dark grey border */
        --shadow: rgba(0, 0, 0, 0.4) 0px 4px 12px; /* More pronounced shadow for dark theme */
        --hover-shadow: rgba(0, 0, 0, 0.6) 0px 6px 18px;
        --success-bg: #284D31; --success-text: #C8E6C9; --success-border: #388E3C;
        --error-bg: #6B2E35; --error-text: #FFCDD2; --error-border: #D32F2F;
        --info-bg: #2A5A6A; --info-text: #BBDEFB; --info-border: #1976D2;
    """

    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Poppins:wght@400;600;700&display=swap');

            /* Apply selected theme variables */
            :root {{
                {"/* Light Theme */" if theme == "light" else "/* Dark Theme */"}
                {light_theme_vars if theme == "light" else dark_theme_vars}
                --border-radius: 0.75rem; /* Slightly more rounded corners */
            }}

            body {{
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
            }}

            /* --- Apply colors and styling using variables --- */
            .stApp {{
                background-color: var(--background-color);
                color: var(--text-color);
                transition: background-color 0.4s ease, color 0.4s ease; /* Smoother transition */
            }}

            /* Main content area styling - removed max-width for full screen */
            .main .block-container {{
                padding-top: 2.5rem; /* Slightly more padding */
                padding-bottom: 2.5rem;
                padding-left: 3rem; /* More horizontal padding */
                padding-right: 3rem;
                max-width: 100%; /* Ensure full width for main content */
            }}

            /* Header styling */
            h1, h2, h3, h4, h5, h6 {{
                color: var(--primary-color);
                font-weight: 600;
                margin-bottom: 1rem;
            }}

            /* Specific styling for brand header and subtitle */
            .brand-header {{
                font-family: 'Poppins', sans-serif;
                font-size: 3.8rem; /* Even larger font size for brand */
                font-weight: 700;
                color: var(--primary-color);
                text-align: center;
                margin-bottom: 0.75rem;
                letter-spacing: 2px;
                text-shadow: 3px 3px 6px rgba(0,0,0,0.2); /* More prominent shadow */
                transition: color 0.4s ease, text-shadow 0.4s ease;
            }}

            .brand-subtitle {{
                font-family: 'Inter', sans-serif;
                font-size: 1.6rem; /* Slightly larger subtitle */
                font-weight: 400;
                color: var(--secondary-color);
                text-align: center;
                margin-top: 0;
                margin-bottom: 2.5rem;
                transition: color 0.4s ease;
            }}

            /* Increased font size for question text */
            .stMarkdown p strong {{
                font-size: 1.3rem; /* Larger font size for questions */
                line-height: 1.6;
                color: var(--text-color); /* Ensure question text uses main text color */
            }}

            /* Card-like containers for sections */
            .stContainer {{
                background-color: var(--card-background);
                padding: 2rem; /* More padding inside cards */
                border-radius: var(--border-radius);
                box-shadow: var(--shadow);
                margin-bottom: 2rem; /* More margin between cards */
                transition: all 0.3s ease-in-out;
            }}
            .stContainer:hover {{
                box-shadow: var(--hover-shadow);
            }}

            /* Buttons */
            .stButton > button {{
                background-color: var(--primary-color);
                color: var(--card-background); /* Button text contrasts with primary color */
                border: none;
                border-radius: var(--border-radius);
                padding: 0.8rem 1.8rem; /* Larger padding for buttons */
                font-weight: 600;
                font-size: 1.05rem; /* Slightly larger button text */
                transition: all 0.2s ease-in-out;
                box-shadow: rgba(0, 0, 0, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.1) 0px 3px 7px -3px; /* More refined shadow */
            }}
            .stButton > button:hover {{
                filter: brightness(1.15); /* Slightly brighter on hover for both themes */
                transform: translateY(-3px); /* More pronounced lift */
                box-shadow: var(--hover-shadow);
            }}
            .stButton > button:active {{
                transform: translateY(0);
                box-shadow: var(--shadow);
            }}

            /* Text Inputs and Text Areas */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea {{
                border-radius: var(--border-radius);
                border: 1px solid var(--border-color);
                padding: 0.8rem 1.2rem; /* Larger padding for inputs */
                font-family: 'Inter', sans-serif;
                color: var(--text-color);
                background-color: var(--background-color); /* Inputs match app background */
                transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            }}
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus {{
                border-color: var(--primary-color);
                box-shadow: 0 0 0 0.25rem rgba(var(--primary-color-rgb), 0.25); /* Use primary color for focus outline with transparency */
                outline: none;
            }}
            /* Ensure labels for inputs have correct color */
            .stTextInput label, .stTextArea label {{
                color: var(--text-color);
            }}

            /* Radio Buttons */
            .stRadio > label {{
                font-weight: 400;
                color: var(--text-color);
                font-size: 1.15rem; /* Larger font size for radio options */
            }}
            .stRadio div[role="radiogroup"] label span {{
                border-radius: 50%;
                border: 2px solid var(--primary-color);
                background-color: var(--card-background);
                width: 20px; /* Slightly larger radio button circles */
                height: 20px;
                display: inline-block;
                vertical-align: middle;
                margin-right: 10px; /* More space */
                position: relative;
                transition: all 0.2s ease;
            }}
            .stRadio div[role="radiogroup"] label.st-dg span {{ /* Selected radio button */
                background-color: var(--primary-color);
                border-color: var(--primary-color);
            }}
            .stRadio div[role="radiogroup"] label.st-dg span::after {{
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 10px; /* Larger inner circle */
                height: 10px;
                background-color: var(--card-background);
                border-radius: 50%;
            }}

            /* Expander (for admin section) */
            .streamlit-expanderHeader {{
                background-color: var(--accent-light);
                border-radius: var(--border-radius);
                padding: 0.9rem 1.8rem; /* More padding */
                font-weight: 600;
                color: var(--primary-color);
                border: none;
                box-shadow: var(--shadow);
                transition: all 0.2s ease-in-out;
            }}
            .streamlit-expanderHeader:hover {{
                filter: brightness(1.1); /* Slightly brighter on hover */
                transform: translateY(-2px);
            }}

            /* Sidebar styling */
            .stSidebar > div:first-child {{
                background-color: var(--card-background); /* Sidebar uses card background */
                padding: 2.5rem 2rem; /* More padding */
                box-shadow: var(--shadow);
                border-radius: var(--border-radius);
                transition: background-color 0.4s ease, box-shadow 0.4s ease;
            }}
            .stSidebar .stButton > button {{
                width: 100%;
                margin-bottom: 0.75rem; /* More space between sidebar buttons */
            }}

            /* Metrics */
            [data-testid="stMetric"] {{
                background-color: var(--card-background);
                padding: 1.5rem; /* More padding */
                border-radius: var(--border-radius);
                box-shadow: var(--shadow);
                text-align: center;
                margin-bottom: 1.5rem;
            }}
            [data-testid="stMetric"] > div > div:first-child {{
                color: var(--secondary-color);
                font-size: 1rem; /* Slightly larger label */
            }}
            [data-testid="stMetric"] > div > div:last-child {{
                color: var(--primary-color);
                font-size: 2.2rem; /* Larger value */
                font-weight: 700;
            }}

            /* Success/Error/Info messages */
            .stAlert {{
                border-radius: var(--border-radius);
                padding: 1.2rem; /* More padding */
                margin-bottom: 1.2rem;
                font-size: 1.05rem; /* Slightly larger text */
            }}
            .stAlert.success {{
                background-color: var(--success-bg);
                color: var(--success-text);
                border-color: var(--success-border);
            }}
            .stAlert.error {{
                background-color: var(--error-bg);
                color: var(--error-text);
                border-color: var(--error-border);
            }}
            .stAlert.info {{
                background-color: var(--info-bg);
                color: var(--info-text);
                border-color: var(--info-border);
            }}

            /* Logo Container (for login page) */
            .logo-container {{
                text-align: center;
                margin-bottom: 2.5rem; /* More margin below logo */
                padding-bottom: 1.5rem;
                border-bottom: 1px solid var(--border-color); /* Use dynamic border color */
            }}
            /* Fixed button container at the bottom for quiz */
            .fixed-bottom-buttons {{
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                width: 100%;
                background-color: var(--card-background); /* Match card background */
                padding: 1rem 2rem;
                box-shadow: rgba(0, 0, 0, 0.2) 0px -5px 15px -3px; /* Shadow above buttons */
                display: flex;
                justify-content: flex-end; /* Align to the right */
                gap: 1rem; /* Space between buttons */
                z-index: 1000; /* Ensure buttons are on top */
                border-top-left-radius: var(--border-radius);
                border-top-right-radius: var(--border-radius);
            }}
            .fixed-bottom-buttons .stButton {{
                flex-grow: 0; /* Prevent buttons from growing */
                flex-shrink: 0; /* Prevent buttons from shrinking */
                width: auto; /* Allow button width to be determined by content + padding */
            }}
            .fixed-bottom-buttons .stButton > button {{
                width: auto; /* Make buttons fill their flex container */
                min-width: 180px; /* Ensure a minimum width for better appearance */
            }}

            /* Adjust main content padding when fixed buttons are present */
            .main {{
                padding-bottom: 6rem; /* Add padding to main content to prevent overlap with fixed buttons */
            }}

            /* Hide the internal Streamlit buttons that are triggered by custom HTML */
            /* Targeting the container div of the button by its data-testid */
            [data-testid="stButton-submit_answer_internal_btn"],
            [data-testid="stButton-next_question_internal_btn"] {{
                display: none !important;
            }}
            /* Hide the internal submit/next/finish button that is triggered by custom HTML */
            [data-testid="stButton-next_question_submit_quiz_internal_btn"] {{
                display: none !important;
>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572
            }}
            body {{ font-family: 'Inter', sans-serif; margin: 0; padding: 0; }}
            .stApp {{ background-color: var(--background-color); color: var(--text-color); transition: background-color 0.4s ease, color 0.4s ease; }}
            .main .block-container {{ padding: 2.5rem 3rem; max-width: 100%; }}
            h1, h2, h3, h4, h5, h6 {{ color: var(--primary-color); font-weight: 600; margin-bottom: 1rem; }}
            .brand-header {{ font-family: 'Poppins', sans-serif; font-size: 3.8rem; font-weight: 700; color: var(--primary-color); text-align: center; margin-bottom: 0.75rem; letter-spacing: 2px; text-shadow: 3px 3px 6px rgba(0,0,0,0.2); transition: color 0.4s ease, text-shadow 0.4s ease; }}
            .brand-subtitle {{ font-family: 'Inter', sans-serif; font-size: 1.6rem; font-weight: 400; color: var(--secondary-color); text-align: center; margin-top: 0; margin-bottom: 2.5rem; transition: color 0.4s ease; }}
            .stMarkdown p strong {{ font-size: 1.3rem; line-height: 1.6; color: var(--text-color); }}
            .stContainer {{ background-color: var(--card-background); padding: 2rem; border-radius: var(--border-radius); box-shadow: var(--shadow); margin-bottom: 2rem; transition: all 0.3s ease-in-out; }}
            .stContainer:hover {{ box-shadow: var(--hover-shadow); }}
            .stButton > button {{ background-color: var(--primary-color); color: var(--card-background); border: none; border-radius: var(--border-radius); padding: 0.8rem 1.8rem; font-weight: 600; font-size: 1.05rem; transition: all 0.2s ease-in-out; box-shadow: rgba(0, 0, 0, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.1) 0px 3px 7px -3px; }}
            .stButton > button:hover {{ filter: brightness(1.15); transform: translateY(-3px); box-shadow: var(--hover-shadow); }}
            .stButton > button:active {{ transform: translateY(0); box-shadow: var(--shadow); }}
            .stTextInput > div > div > input, .stTextArea > div > div > textarea {{ border-radius: var(--border-radius); border: 1px solid var(--border-color); padding: 0.8rem 1.2rem; font-family: 'Inter', sans-serif; color: var(--text-color); background-color: var(--background-color); transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out; }}
            .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {{ border-color: var(--primary-color); box-shadow: 0 0 0 0.25rem rgba(var(--primary-color-rgb), 0.25); outline: none; }}
            .stTextInput label, .stTextArea label {{ color: var(--text-color); }}
            .stRadio > label {{ font-weight: 400; color: var(--text-color); font-size: 1.15rem; }}
            .streamlit-expanderHeader {{ background-color: var(--accent-light); border-radius: var(--border-radius); padding: 0.9rem 1.8rem; font-weight: 600; color: var(--primary-color); border: none; box-shadow: var(--shadow); transition: all 0.2s ease-in-out; }}
            .stSidebar > div:first-child {{ background-color: var(--card-background); padding: 2.5rem 2rem; box-shadow: var(--shadow); border-radius: var(--border-radius); transition: background-color 0.4s ease, box-shadow 0.4s ease; }}
            [data-testid="stMetric"] {{ background-color: var(--card-background); padding: 1.5rem; border-radius: var(--border-radius); box-shadow: var(--shadow); text-align: center; margin-bottom: 1.5rem; }}
            .stAlert {{ border-radius: var(--border-radius); padding: 1.2rem; margin-bottom: 1.2rem; font-size: 1.05rem; }}
            .logo-container {{ text-align: center; margin-bottom: 2.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); }}
            .fixed-bottom-buttons {{ position: fixed; bottom: 0; left: 0; right: 0; width: 100%; background-color: var(--card-background); padding: 1rem 2rem; box-shadow: rgba(0, 0, 0, 0.2) 0px -5px 15px -3px; display: flex; justify-content: flex-end; gap: 1rem; z-index: 1000; border-top-left-radius: var(--border-radius); border-top-right-radius: var(--border-radius); }}
            .main {{ padding-bottom: 6rem; }}
        </style>
    """, unsafe_allow_html=True)

# --- Session State Initialization ---
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
    if "current_page" not in st.session_state:
<<<<<<< HEAD
        st.session_state.current_page = "Home"
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
=======
        st.session_state.current_page = "Home" # Default page after login
    if "theme" not in st.session_state:
        st.session_state.theme = "light" # Default theme
>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572

    # Student Quiz State
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
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None # No option selected by default
    if "feedback_message" not in st.session_state:
        st.session_state.feedback_message = ""
    if "quiz_completed" not in st.session_state:
        st.session_state.quiz_completed = False

<<<<<<< HEAD
=======
    # Data loaded from files
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r") as f:
            initial_questions_data = json.load(f)
        if isinstance(initial_questions_data, list):
            # This conversion warning should now appear after set_page_config
            st.warning(f"Converting '{QUESTIONS_FILE}' from old list format to new multi-quiz format. Please review.")
            initial_questions_data = {"SAP Security Quiz": initial_questions_data}
            save_json_file(QUESTIONS_FILE, initial_questions_data)
    else:
        initial_questions_data = {"SAP Security Quiz": []}
        save_json_file(QUESTIONS_FILE, initial_questions_data)

    st.session_state.questions = initial_questions_data
    st.session_state.users = load_json_file(USERS_FILE, {"admin": {"password": "adminpassword", "role": "admin"}})
    st.session_state.user_progress = load_json_file(USER_PROGRESS_FILE, {})


>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572
def reset_quiz_state():
    """Resets quiz-specific session state variables."""
    st.session_state.quiz_started = False
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.student_answers = []
    st.session_state.show_explanation = False
    st.session_state.selected_option = None # Ensure no option is selected for a new question
    st.session_state.feedback_message = ""
    st.session_state.quiz_completed = False

def display_logo():
    st.markdown("""
        <div class="logo-container">
            <h1 class="brand-header">NeuroverseAI</h1>
            <p class="brand-subtitle">GenAI & SAP Training</p>
        </div>
    """, unsafe_allow_html=True)

# --- Login Page ---
def login_page():
    """Displays the login form."""
    display_logo()
<<<<<<< HEAD
=======
    
    # Use a container for the login card
>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572
    with st.container():
        st.markdown("<h2 style='text-align: center; color: var(--primary-color);'>🔐 Quiz Platform Login</h2>", unsafe_allow_html=True)
        st.markdown("---")
        with st.form("login_form"):
            username = st.text_input("User ID", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit_button = st.form_submit_button("Login")

            if submit_button:
                user = db.get_user(username)
                if user and user["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.user_role = user["role"]
                    st.session_state.username = user["username"]
                    st.session_state.user_id = user["id"]
                    st.session_state.current_page = "Home"
                    st.success(f"Welcome, {st.session_state.username}!")
                    st.rerun()
                else:
                    st.error("Invalid User ID or Password.")

# --- Home Page ---
def home_page():
    st.title(f"Welcome, {st.session_state.username}!")
    st.header("NeuroverseAI Training Platform")
    st.write("This platform provides quizzes to test your knowledge in GenAI and SAP.")
    st.markdown("---")
    st.subheader("What would you like to do?")
    if st.session_state.user_role == 'student':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Take a Quiz"):
                st.session_state.current_page = "Take Quiz"
                st.rerun()
        with col2:
            if st.button("View My Scores"):
                st.session_state.current_page = "View My Scores"
                st.rerun()
    elif st.session_state.user_role == 'admin':
        st.write("Use the sidebar to navigate to Admin actions.")

# --- Helper function for Next Question / Submit Quiz internal button ---
def handle_next_or_finish_quiz_button(is_last_question):
    """Handles the logic for the Next Question or Submit Quiz button."""
    if is_last_question:
        st.session_state.quiz_completed = True
    else:
        st.session_state.current_question_index += 1
    st.session_state.show_explanation = False
    st.session_state.selected_option = None # Clear selection for next question
    st.session_state.feedback_message = ""

# --- Student Quiz Flow ---
def student_quiz_page():
    st.title(f"Take a Quiz, {st.session_state.username}!")

    available_quizzes = db.get_all_quizzes()
    if not available_quizzes:
        st.warning("No quizzes available. Please ask an administrator to add questions.")
        return

    if st.session_state.current_quiz_id is None:
        st.subheader("Select a Quiz")
        quiz_options = {quiz['name']: quiz['id'] for quiz in available_quizzes}
        selected_quiz_name = st.selectbox("Choose a quiz to start:", list(quiz_options.keys()), key="quiz_selector")
        if st.button("Start Selected Quiz"):
            st.session_state.current_quiz_id = quiz_options[selected_quiz_name]
            reset_quiz_state()
            st.session_state.quiz_started = True
            st.rerun()
        return

    current_quiz_id = st.session_state.current_quiz_id
    current_quiz_name = next((q['name'] for q in available_quizzes if q['id'] == current_quiz_id), "Unknown Quiz")
    questions = db.get_questions_for_quiz(current_quiz_id)
    total_questions = len(questions)

    if not questions:
        st.warning(f"No questions found for '{current_quiz_name}'. Please select another quiz.")
        st.session_state.current_quiz_id = None
        return

<<<<<<< HEAD
    st.header(f"Quiz: {current_quiz_name}")
    st.progress(st.session_state.current_question_index / total_questions)
=======
    st.header(f"Quiz: {current_quiz_id}")

    # Display progress bar
    st.progress((st.session_state.current_question_index) / total_questions, text=f"Progress: {st.session_state.current_question_index}/{total_questions} questions answered.")


    # Check if the student has already completed THIS quiz
    user_quiz_progress = st.session_state.user_progress.get(st.session_state.username, {}).get(current_quiz_id, {})
    if isinstance(user_quiz_progress, dict) and user_quiz_progress.get("attempted", False) and user_quiz_progress.get("total", 0) == total_questions:
        st.info(f"You have already completed the '{current_quiz_id}' quiz.")
        col_score, col_accuracy = st.columns(2)
        with col_score:
            st.metric("Your Previous Score", f"{user_quiz_progress['score']} / {user_quiz_progress['total']}")
        with col_accuracy:
            prev_accuracy = (user_quiz_progress['score'] / user_quiz_progress['total'] * 100) if user_quiz_progress['total'] > 0 else 0
            st.metric("Your Previous Accuracy", f"{prev_accuracy:.2f}%")
        st.write("You can view detailed results in 'View My Scores'.")
        if st.button("Choose another Quiz"):
            st.session_state.current_quiz_id = None
            st.session_state.quiz_started = False
            st.rerun()
        return
>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572

    if st.session_state.quiz_completed:
        display_quiz_dashboard(total_questions, current_quiz_name)
        db.save_user_progress(st.session_state.user_id, current_quiz_id, st.session_state.score, total_questions, True, json.dumps(st.session_state.student_answers))
        st.success(f"Your results for '{current_quiz_name}' have been saved!")

        if st.button("Take another Quiz"):
            st.session_state.current_quiz_id = None
            reset_quiz_state()
            st.rerun()
        return

    current_q_index = st.session_state.current_question_index
    if current_q_index >= total_questions:
        st.session_state.quiz_completed = True
        st.rerun()

    current_question = questions[current_q_index]
<<<<<<< HEAD
    options = json.loads(current_question["options"])

    with st.container():
        st.subheader(f"Question {current_q_index + 1} of {total_questions}")
        st.markdown(f"**{current_question['question_text']}**")
        
        selected_option = st.radio("Select your answer:", options, key=f"radio_q_{current_q_index}", disabled=st.session_state.show_explanation)

        if st.session_state.show_explanation:
            st.write(st.session_state.feedback_message)
            st.info(f"Explanation: {current_question['explanation']}")
            
            is_last_question = (current_q_index + 1 == total_questions)
            next_button_text = "Submit Quiz" if is_last_question else "Next Question"
            if st.button(next_button_text):
                if is_last_question:
                    st.session_state.quiz_completed = True
                else:
                    st.session_state.current_question_index += 1
                st.session_state.show_explanation = False
                st.rerun()
        else:
            if st.button("Submit Answer"):
                is_correct = (selected_option == current_question["correct_option"])
                if is_correct:
                    st.session_state.score += 1
                    st.session_state.feedback_message = "✅ Correct!"
                else:
                    st.session_state.feedback_message = f"❌ Wrong! The correct answer was: **{current_question['correct_option']}**"
                
                st.session_state.student_answers.append({
                    "question": current_question["question_text"],
                    "selected_answer": selected_option,
                    "correct_answer": current_question["correct_option"],
                    "is_correct": is_correct,
                    "explanation": current_question["explanation"]
                })
                st.session_state.show_explanation = True
                st.rerun()

def display_quiz_dashboard(total_questions, quiz_name):
    st.subheader(f"Quiz Completed: {quiz_name}!")
    score = st.session_state.score
    accuracy = (score / total_questions * 100) if total_questions > 0 else 0
=======
    is_last_question = (current_q_index + 1 == total_questions)

    def update_selected_option_and_record():
        # This callback updates st.session_state.selected_option
        # with the value from the radio button when its value changes.
        st.session_state.selected_option = st.session_state[f"radio_q_{st.session_state.current_question_index}_{current_quiz_id}"]

    with st.container():
        st.subheader(f"Question {current_q_index + 1} of {total_questions}")
        st.markdown(f"**{current_question['question']}**")

        # Determine initial index for st.radio
        # It should be None by default, and only set if an option was previously selected
        initial_radio_index = None
        if st.session_state.selected_option in current_question["options"]:
            initial_radio_index = current_question["options"].index(st.session_state.selected_option)

        st.radio(
            "Select your answer:",
            current_question["options"],
            index=initial_radio_index, # Use the determined initial index
            key=f"radio_q_{current_q_index}_{current_quiz_id}", # Unique key for the radio button
            on_change=update_selected_option_and_record, # Call this function when radio selection changes
            disabled=st.session_state.show_explanation # Disable after submission
        )

        # Submit Answer button (below options, not fixed)
        if not st.session_state.show_explanation:
            if st.button(
                "Submit Answer",
                key="submit_answer_button",
                disabled=st.session_state.selected_option is None,
                on_click=lambda q=current_question: st.session_state.update(
                    attempted_questions_count=st.session_state.attempted_questions_count + 1,
                    score=st.session_state.score + (1 if st.session_state.selected_option == q["correct_option"] else 0),
                    feedback_message="✅ Correct!" if st.session_state.selected_option == q["correct_option"] else f"❌ Wrong! The correct answer was: **{q['correct_option']}**",
                    show_explanation=True,
                    student_answers=st.session_state.student_answers + [{
                        "question": q["question"],
                        "selected_answer": st.session_state.selected_option,
                        "correct_answer": q["correct_option"],
                        "is_correct": (st.session_state.selected_option == q["correct_option"]),
                        "explanation": q["explanation"]
                    }]
                )
            ):
                pass # This block is necessary for Streamlit button to trigger on_click

        # Display feedback and explanation
        if st.session_state.show_explanation:
            st.write(st.session_state.feedback_message)
            st.info(f"Explanation: {current_question['explanation']}")

    # Fixed bottom button for Next Question / Submit Quiz
    if st.session_state.show_explanation: # Only show after an answer has been submitted
        next_or_finish_button_text = "Submit Quiz" if is_last_question else "Next Question"
        # Using a container with custom HTML to apply fixed positioning and right alignment
        st.markdown('<div class="fixed-bottom-buttons">', unsafe_allow_html=True)
        if st.button(
            next_or_finish_button_text,
            key="next_question_submit_quiz_button",
            on_click=lambda: handle_next_or_finish_quiz_button(is_last_question) # Pass is_last_question
        ):
            pass # This block is necessary for Streamlit button to trigger on_click
        st.markdown('</div>', unsafe_allow_html=True)


def display_quiz_dashboard(total_questions, quiz_id):
    """Displays the final quiz dashboard."""
    st.subheader(f"Quiz Completed: {quiz_id}!")
>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572
    
    col1, col2 = st.columns(2)
    col1.metric("Total Score", f"{score}/{total_questions}")
    col2.metric("Accuracy", f"{accuracy:.2f}%")

    st.write("---")
    st.subheader("Your Answers:")
    for i, answer in enumerate(st.session_state.student_answers):
        with st.container():
            st.markdown(f"**Q{i+1}:** {answer['question']}")
            st.markdown(f"Your Answer: **{answer['selected_answer']}** {'✅' if answer['is_correct'] else '❌'}")
            if not answer['is_correct']:
                st.markdown(f"Correct Answer: **{answer['correct_answer']}**")
            st.info(f"Explanation: {answer['explanation']}")
            st.markdown("---")

def view_my_scores_page():
    st.title(f"My Quiz Scores, {st.session_state.username}!")
    user_progress = db.get_user_progress(st.session_state.user_id)

    if not user_progress:
        st.info("You haven't attempted any quizzes yet.")
        return

    progress_data = []
    for row in user_progress:
        accuracy = (row['score'] / row['total'] * 100) if row['total'] > 0 else 0
        progress_data.append({
            "Quiz Name": row['quiz_name'],
            "Score": f"{row['score']}/{row['total']}",
            "Accuracy": f"{accuracy:.2f}%"
        })
    
    st.subheader("Summary of Completed Quizzes")
    df_summary = pd.DataFrame(progress_data)
    st.dataframe(df_summary, hide_index=True)

    st.markdown("---")
    st.subheader("Review Past Quiz Attempts")
    
    review_options = {row['quiz_name']: row for row in user_progress}
    selected_quiz_to_review = st.selectbox("Select a completed quiz to review:", list(review_options.keys()))

    if selected_quiz_to_review:
        quiz_log_data = review_options[selected_quiz_to_review]
        quiz_log = json.loads(quiz_log_data["answers_log"])
        
        st.markdown(f"#### Detailed Review for: {selected_quiz_to_review}")
        st.metric("Score", f"{quiz_log_data['score']}/{quiz_log_data['total']}")

        for i, answer_log in enumerate(quiz_log):
             with st.container():
                st.markdown(f"**Q{i+1}:** {answer_log['question']}")
                st.markdown(f"Your Answer: **{answer_log['selected_answer']}** {'✅' if answer_log['is_correct'] else '❌'}")
                if not answer_log['is_correct']:
                    st.markdown(f"Correct Answer: **{answer_log['correct_answer']}**")
                st.info(f"Explanation: {answer_log['explanation']}")
                st.markdown("---")

# --- Admin Flow ---
def admin_page():
    st.title(f"Welcome, {st.session_state.username} (Admin)!")
    st.sidebar.header("Admin Actions")
    admin_action = st.sidebar.radio("Choose an action:", ["Manage Questions", "Manage Users", "View Trainee Performance"])

    if admin_action == "Manage Questions":
        manage_questions_section()
    elif admin_action == "Manage Users":
        manage_users_section()
    elif admin_action == "View Trainee Performance":
        view_trainee_performance_section()

def manage_questions_section():
    st.header("Manage Quiz Questions")

    # Create new quiz
    with st.expander("Create New Quiz"):
        new_quiz_name = st.text_input("New Quiz Name")
        if st.button("Create Quiz"):
            if new_quiz_name:
                db.add_quiz(new_quiz_name)
                st.success(f"Quiz '{new_quiz_name}' created successfully.")
                st.rerun()
            else:
                st.warning("Quiz name cannot be empty.")

    all_quizzes = db.get_all_quizzes()
    if not all_quizzes:
        st.info("No quizzes found. Create one to get started.")
        return

    quiz_options = {quiz['name']: quiz['id'] for quiz in all_quizzes}
    selected_quiz_name = st.selectbox("Select Quiz to Manage", list(quiz_options.keys()))
    selected_quiz_id = quiz_options[selected_quiz_name]

<<<<<<< HEAD
    # Add question to selected quiz
    with st.expander(f"Add New Question to '{selected_quiz_name}'"):
        with st.form("add_question_form", clear_on_submit=True):
            question_text = st.text_area("Question Text")
            options_text = st.text_input("Options (comma-separated)", help="e.g., Option 1,Option 2,Option 3")
            options = [opt.strip() for opt in options_text.split(',') if opt.strip()]
            correct_option = st.selectbox("Correct Option", options)
            explanation = st.text_area("Explanation")
            add_button = st.form_submit_button("Add Question")

            if add_button:
                if question_text and options and correct_option and explanation:
                    db.add_question(selected_quiz_id, question_text, options, correct_option, explanation)
                    st.success("Question added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill all fields.")
    
    st.subheader(f"Existing Questions in '{selected_quiz_name}'")
    questions = db.get_questions_for_quiz(selected_quiz_id)
    if not questions:
        st.info("No questions in this quiz yet.")
    
    for q in questions:
        st.markdown(f"**Q: {q['question_text']}**")
        st.write(f"Correct Answer: {q['correct_option']}")
        if st.button("Delete", key=f"del_q_{q['id']}"):
            db.delete_question(q['id'])
            st.rerun()
        st.markdown("---")

def manage_users_section():
=======
    # --- Delete Quiz Section ---
    if selected_quiz_for_management:
        st.markdown("---")
        st.subheader(f"Danger Zone: Delete '{selected_quiz_for_management}' Quiz")
        # Use a checkbox for confirmation to avoid accidental clicks
        confirm_delete_quiz_checkbox = st.checkbox(f"I understand that deleting '{selected_quiz_for_management}' is irreversible and will remove all associated student progress.", key=f"confirm_delete_quiz_checkbox_{selected_quiz_for_management}")
        if st.button(f"Delete Quiz '{selected_quiz_for_management}' Permanently", key=f"delete_quiz_button_{selected_quiz_for_management}", disabled=not confirm_delete_quiz_checkbox):
            if confirm_delete_quiz_checkbox:
                del st.session_state.questions[selected_quiz_for_management]
                save_json_file(QUESTIONS_FILE, st.session_state.questions)
                
                # Remove associated user progress for this quiz
                for user_id in list(st.session_state.user_progress.keys()): # Iterate over a copy of keys
                    if selected_quiz_for_management in st.session_state.user_progress[user_id]:
                        del st.session_state.user_progress[user_id][selected_quiz_for_management]
                save_json_file(USER_PROGRESS_FILE, st.session_state.user_progress)
                
                st.success(f"Quiz '{selected_quiz_for_management}' and its associated progress deleted successfully.")
                st.session_state.current_quiz_id = None # Clear current quiz if it was deleted
                st.rerun()
            else:
                st.error("Please confirm deletion by checking the box.")
        st.markdown("---")


    with st.container():
        st.subheader(f"Add New Question to '{selected_quiz_for_management}'")
        with st.form("add_question_form"):
            new_question_text = st.text_area("Question Text", key="add_q_text")
            # Allow adding fewer than 4 options initially
            new_options_inputs = []
            for i in range(4): # Provide inputs for up to 4 options
                option_value = st.text_input(f"Option {i+1}", key=f"add_opt_{i}")
                if option_value: # Only add non-empty options
                    new_options_inputs.append(option_value)

            new_correct_option = st.selectbox("Correct Option", options=new_options_inputs if new_options_inputs else ["Select an option"], key="add_correct_opt")
            new_explanation = st.text_area("Explanation", key="add_explanation")
            add_button = st.form_submit_button("Add Question")

            if add_button:
                if not (new_question_text and new_options_inputs and new_correct_option and new_explanation):
                    st.error("Please fill in all mandatory fields (Question, at least one Option, Correct Option, and Explanation).")
                elif new_correct_option not in new_options_inputs:
                    st.error("Correct option must be one of the provided options.")
                else:
                    new_q = {
                        "question": new_question_text,
                        "options": new_options_inputs, # Save only the provided options
                        "correct_option": new_correct_option, # Storing as string
                        "explanation": new_explanation
                    }
                    st.session_state.questions[selected_quiz_for_management].append(new_q)
                    save_json_file(QUESTIONS_FILE, st.session_state.questions)
                    st.success("Question added successfully!")
                    st.rerun()

    st.subheader(f"Existing Questions in '{selected_quiz_for_management}'")
    if not questions_for_selected_quiz:
        st.info("No questions available for this quiz. Add some using the form above.")
        return

    for i, q in enumerate(questions_for_selected_quiz):
        with st.container():
            with st.expander(f"Question {i+1}: {q['question'][:70]}..."): # Truncate for display
                st.write(f"**Question:** {q['question']}")
                st.write(f"**Options:** {', '.join(q['options'])}")
                st.write(f"**Correct Option:** {q['correct_option']}")
                st.write(f"**Explanation:** {q['explanation']}")

                st.markdown("---")
                st.write("Edit this question:")
                edited_question = st.text_area("Question Text", value=q["question"], key=f"edit_q_text_{selected_quiz_for_management}_{i}")
                
                # Dynamically generate text inputs for existing options, and empty for up to 4 if less exist
                edited_options = []
                for j in range(max(len(q["options"]), 4)): # Ensure at least 4 input fields are shown for editing
                    option_value = q["options"][j] if j < len(q["options"]) else ""
                    edited_option_input = st.text_input(f"Option {j+1}", value=option_value, key=f"edit_opt_{selected_quiz_for_management}_{i}_{j}")
                    if edited_option_input: # Only include non-empty options in the final list
                        edited_options.append(edited_option_input)

                try:
                    # Find the index of the current correct option within the *edited* options
                    current_correct_index = edited_options.index(q["correct_option"])
                except ValueError:
                    # If the correct option string is not found in the current edited options, default to the first option or None
                    current_correct_index = 0 if edited_options else None

                edited_correct_option = st.selectbox(
                    "Correct Option",
                    options=edited_options if edited_options else ["Select an option"],
                    index=current_correct_index,
                    key=f"edit_correct_opt_{selected_quiz_for_management}_{i}"
                )
                edited_explanation = st.text_area("Explanation", value=q["explanation"], key=f"edit_explanation_{selected_quiz_for_management}_{i}")

                col_edit, col_delete = st.columns(2)
                with col_edit:
                    if st.button("Save Changes", key=f"save_q_{selected_quiz_for_management}_{i}"):
                        if not (edited_question and edited_options and edited_correct_option and edited_explanation):
                            st.error("Please fill in all mandatory fields (Question, at least one Option, Correct Option, and Explanation).")
                        elif edited_correct_option not in edited_options:
                            st.error("Correct option must be one of the provided options.")
                        else:
                            st.session_state.questions[selected_quiz_for_management][i] = {
                                "question": edited_question,
                                "options": edited_options, # Save only the valid, non-empty options
                                "correct_option": edited_correct_option,
                                "explanation": edited_explanation
                            }
                            save_json_file(QUESTIONS_FILE, st.session_state.questions)
                            st.success(f"Question {i+1} updated successfully!")
                            st.rerun()
                with col_delete:
                    if st.button("Delete Question", key=f"delete_q_{selected_quiz_for_management}_{i}"):
                        st.session_state.questions[selected_quiz_for_management].pop(i)
                        save_json_file(QUESTIONS_FILE, st.session_state.questions)
                        st.warning(f"Question {i+1} deleted from '{selected_quiz_for_management}'.")
                        st.rerun()

def manage_users_section():
    """Admin section to create student accounts and manage existing ones."""
>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572
    st.header("Manage User Accounts")

    with st.expander("Create New Student Account"):
        with st.form("create_student_form", clear_on_submit=True):
            new_username = st.text_input("New Student User ID")
            new_password = st.text_input("New Student Password", type="password")
            create_button = st.form_submit_button("Create Student Account")

            if create_button:
                if new_username and new_password:
                    if not db.get_user(new_username):
                        db.add_user(new_username, new_password, "student")
                        st.success(f"Student account '{new_username}' created successfully!")
                    else:
                        st.error(f"User ID '{new_username}' already exists.")
                else:
                    st.error("Please provide both username and password.")
<<<<<<< HEAD
    
    st.subheader("Existing Users")
    users = db.get_all_users()
    for user in users:
        if user['role'] == 'student': # Only show students for deletion
            col1, col2, col3 = st.columns([2,2,1])
            col1.write(user['username'])
            col2.write(user['role'])
            if col3.button("Delete", key=f"del_u_{user['id']}"):
                db.delete_user(user['id'])
                st.rerun()
            st.markdown("---")
=======

    st.subheader("Existing Users")
    if not st.session_state.users:
        st.info("No users found.")
        return

    # Display users with a delete option
    # Create columns for header
    col_header_user, col_header_role, col_header_action = st.columns([0.4, 0.3, 0.3])
    with col_header_user:
        st.markdown("**Username**")
    with col_header_role:
        st.markdown("**Role**")
    with col_header_action:
        st.markdown("**Action**")
    st.markdown("---")

    for u in list(st.session_state.users.keys()): # Iterate over a copy of keys for safe deletion
        user_data = st.session_state.users[u]
        col_user, col_role, col_delete_btn = st.columns([0.4, 0.3, 0.3])
        
        with col_user:
            st.write(u)
        with col_role:
            st.write(user_data["role"])
        
        with col_delete_btn:
            if u == st.session_state.username: # Current logged-in admin cannot delete themselves
                st.info("Current User")
            elif user_data["role"] == "admin": # Prevent deleting other admins for simplicity
                 st.info("Admin User")
            else:
                # Use a unique key for each delete checkbox and button
                delete_key_checkbox = f"delete_user_checkbox_{u}"
                delete_key_button = f"delete_user_button_{u}"

                confirm_delete_user_checkbox = st.checkbox(f"Confirm delete {u}", key=delete_key_checkbox)
                if st.button(f"Delete {u}", key=delete_key_button, disabled=not confirm_delete_user_checkbox):
                    if confirm_delete_user_checkbox:
                        del st.session_state.users[u]
                        save_json_file(USERS_FILE, st.session_state.users)
                        # Remove user's progress data
                        if u in st.session_state.user_progress:
                            del st.session_state.user_progress[u]
                            save_json_file(USER_PROGRESS_FILE, st.session_state.user_progress)
                        st.success(f"User '{u}' and their progress deleted successfully.")
                        st.rerun()
                    else:
                        st.error("Please confirm deletion by checking the box.")
        st.markdown("---")

>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572

def view_trainee_performance_section():
    st.header("Trainee Performance Overview")
    progress_data = db.get_all_user_progress()
    if progress_data:
        df = pd.DataFrame(progress_data)
        df['Accuracy'] = (df['score'] / df['total'] * 100).map('{:.2f}%'.format)
        df_display = df[['student_id', 'quiz_name', 'score', 'total', 'Accuracy']]
        st.dataframe(df_display, hide_index=True)
    else:
        st.info("No quiz attempts have been recorded yet.")


# --- Main Application Logic ---
def main():
<<<<<<< HEAD
    st.set_page_config(page_title="NeuroverseAI Quiz", layout="wide", initial_sidebar_state="collapsed")
    
    # Initialize database and session state
    db.create_tables()
    initialize_session_state() 
    apply_custom_css(st.session_state.theme)

    # Add a default admin if one doesn't exist
    if not db.get_user("admin"):
        db.add_user("admin", "adminpassword", "admin")

    # Sidebar for logout and navigation
    with st.sidebar:
=======
    # set_page_config must be the first Streamlit command
    # Set layout to "wide" for full screen and sidebar to "collapsed" for mobile view
    st.set_page_config(page_title="NeuroverseAI Quiz", layout="wide", initial_sidebar_state="collapsed")
    
    # Initialize session state and load data
    initialize_session_state() 

    # Apply custom CSS immediately after page config, passing the current theme
    apply_custom_css(st.session_state.theme)

    # Sidebar for logout and navigation
    with st.sidebar:
        # Theme toggle button
>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572
        if st.session_state.theme == "light":
            if st.button("🌙 Switch to Dark Mode"):
                st.session_state.theme = "dark"
                st.rerun()
        else:
            if st.button("☀️ Switch to Light Mode"):
                st.session_state.theme = "light"
                st.rerun()
<<<<<<< HEAD
        
=======

>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572
        if st.session_state.logged_in:
            display_logo()
            st.write(f"Logged in as: **{st.session_state.username}** ({st.session_state.user_role.capitalize()})")
            st.markdown("---")
            
            # Navigation logic here for different roles
            
            st.markdown("---")
            if st.button("Logout", key="sidebar_logout_button"):
                st.session_state.logged_in = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.session_state.user_id = None
                st.session_state.current_page = "Login"
                reset_quiz_state()
                st.rerun()
        else:
<<<<<<< HEAD
=======
            # Only show logo and theme toggle on login page if not logged in
>>>>>>> 1d2898f929d22291d213a5a206812f1af9bb0572
            display_logo() 

    # Main content area routing
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.user_role == 'admin':
            admin_page()
        else: # Student view
            page_options = {
                "Home": home_page,
                "Take Quiz": student_quiz_page,
                "View My Scores": view_my_scores_page
            }
            # Add a persistent radio button for navigation for students
            st.session_state.current_page = st.radio(
                "Navigate", 
                options=list(page_options.keys()), 
                horizontal=True,
                key="student_nav"
            )
            page_options[st.session_state.current_page]()


if __name__ == "__main__":
    main()