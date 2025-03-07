import streamlit as st
import pandas as pd
import datetime
import os
import uuid
import sqlite3

# Create a directory for survey responses if it doesn't exist (for CSV backup, optional)
RESPONSES_DIR = 'survey_responses'
os.makedirs(RESPONSES_DIR, exist_ok=True)

# Set page configuration
st.set_page_config(
    page_title="Personal & Professional Insights Survey",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Function to create a unique ID for each respondent
def generate_unique_id():
    return str(uuid.uuid4())

# Initialize SQLite database and create table if it doesn't exist
def init_db():
    conn = sqlite3.connect('survey_responses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unique_id TEXT,
            timestamp TEXT,
            name TEXT,
            age INTEGER,
            occupation TEXT,
            q1 TEXT,
            q2 TEXT,
            q3 TEXT,
            q4 TEXT,
            q5 TEXT,
            q6 TEXT,
            q7 TEXT,
            q8 TEXT,
            q9 TEXT,
            q10 TEXT,
            q11 TEXT,
            q12 TEXT,
            q13 TEXT,
            q14 TEXT,
            q15 TEXT,
            q16 TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to save responses to SQLite database
def save_response_db(responses):
    conn = sqlite3.connect('survey_responses.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO responses (
            unique_id, timestamp, name, age, occupation,
            q1, q2, q3, q4, q5, q6, q7, q8,
            q9, q10, q11, q12, q13, q14, q15, q16
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        responses.get('unique_id'),
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        responses.get('name'),
        responses.get('age'),
        responses.get('occupation'),
        responses.get('q1'),
        responses.get('q2'),
        responses.get('q3'),
        responses.get('q4'),
        responses.get('q5'),
        responses.get('q6'),
        responses.get('q7'),
        responses.get('q8'),
        responses.get('q9'),
        responses.get('q10'),
        responses.get('q11'),
        responses.get('q12'),
        responses.get('q13'),
        responses.get('q14'),
        responses.get('q15'),
        responses.get('q16')
    ))
    conn.commit()
    conn.close()
    return True

# Original CSV save function for backup (optional)
def save_response_csv(responses):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{RESPONSES_DIR}/survey_response_{timestamp}.csv"
    df_new = pd.DataFrame([responses])
    df_new.to_csv(filename, index=False)
    master_filename = f"{RESPONSES_DIR}/all_survey_responses.csv"
    if os.path.exists(master_filename):
        df_existing = pd.read_csv(master_filename)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(master_filename, index=False)
    else:
        df_new.to_csv(master_filename, index=False)
    return True

# Main function for the survey app
def main():
    init_db()  # Initialize the SQLite database at app start
    if 'page' not in st.session_state:
        st.session_state.page = 0
        st.session_state.responses = {}
        st.session_state.unique_id = generate_unique_id()
    
    with st.sidebar:
        st.title("Survey Navigation")
        st.write("Progress through the survey using the buttons at the bottom of each page.")
        total_pages = 7  # Introduction + Demographics + 4 sections of questions + Thank you
        progress = min(st.session_state.page / total_pages, 1.0)
        st.progress(progress)
        st.write(f"Page {st.session_state.page} of {total_pages}")
        if st.button("Reset Survey"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = 0
            st.session_state.responses = {}
            st.session_state.unique_id = generate_unique_id()
            st.rerun()
    
    if st.session_state.page == 0:
        st.title("Personal & Professional Insights Survey")
        st.markdown("""
        ## Welcome to our survey!
        
        This survey aims to gather insights about your personal and professional perspectives. 
        Your responses will help us understand various aspects of personal development and professional growth.
        
        * The survey consists of 16 questions divided into 4 sections
        * All responses are confidential and will be used for research purposes only
        * The survey should take approximately 5-10 minutes to complete
        
        Thank you for participating!
        """)
        st.button("Start Survey", on_click=lambda: setattr(st.session_state, 'page', 1))
    
    elif st.session_state.page == 1:
        st.title("Participant Information")
        st.write("Please provide the following information about yourself:")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        occupation = st.text_input("Occupation (If no occupation, please describe what best describes you)")
        st.session_state.responses.update({
            "name": name,
            "age": age,
            "occupation": occupation
        })
        col1, col2 = st.columns(2)
        with col1:
            st.button("Previous", on_click=lambda: setattr(st.session_state, 'page', 0))
        with col2:
            if name and age and occupation:
                st.button("Next", on_click=lambda: setattr(st.session_state, 'page', 2))
            else:
                st.write("Please fill out all fields to continue.")
    
    elif st.session_state.page == 2:
        st.title("Section 1: Self-awareness and Aspirations")
        st.markdown("### Question 1")
        st.write("Can you tell me about a project or task you started and finished on your own? What did you do and what was the result?")
        q1 = st.text_area("Your answer", key="q1", height=150)
        st.markdown("### Question 2")
        st.write("What kind of life do you dream about having when you grow up?")
        q2 = st.text_area("Your answer", key="q2", height=150)
        st.markdown("### Question 3")
        st.write("What do people always say you're great at?")
        q3 = st.text_area("Your answer", key="q3", height=150)
        st.markdown("### Question 4")
        st.write("What is one thing you would like to be better at? Why that one?")
        q4 = st.text_area("Your answer", key="q4", height=150)
        st.session_state.responses.update({
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "q4": q4
        })
        col1, col2 = st.columns(2)
        with col1:
            st.button("Previous", on_click=lambda: setattr(st.session_state, 'page', 1))
        with col2:
            st.button("Next", on_click=lambda: setattr(st.session_state, 'page', 3))
    
    elif st.session_state.page == 3:
        st.title("Section 2: Success and Responsibility")
        st.markdown("### Question 5")
        st.write("How do you define success? Has the way you think about success changed as you've gotten older?")
        q5 = st.text_area("Your answer", key="q5", height=150)
        st.markdown("### Question 6")
        st.write("What does being responsible mean to you when it comes to work or personal projects?")
        q6 = st.text_area("Your answer", key="q6", height=150)
        st.markdown("### Question 7")
        st.write("Thinking about a hobby or interest you're passionate about, how did you get started and what keeps you engaged?")
        q7 = st.text_area("Your answer", key="q7", height=150)
        st.markdown("### Question 8")
        st.write("What's something you do all the time but wish you could get paid for?")
        q8 = st.text_area("Your answer", key="q8", height=150)
        st.session_state.responses.update({
            "q5": q5,
            "q6": q6,
            "q7": q7,
            "q8": q8
        })
        col1, col2 = st.columns(2)
        with col1:
            st.button("Previous", on_click=lambda: setattr(st.session_state, 'page', 2))
        with col2:
            st.button("Next", on_click=lambda: setattr(st.session_state, 'page', 4))
    
    elif st.session_state.page == 4:
        st.title("Section 3: Goals and Challenges")
        st.markdown("### Question 9")
        st.write("Imagine you have a task that you find uninteresting but necessary. How do you motivate yourself to complete it?")
        q9 = st.text_area("Your answer", key="q9", height=150)
        st.markdown("### Question 10")
        st.write("What's one long-term goal you have, and what are the smaller steps you're taking to reach it?")
        q10 = st.text_area("Your answer", key="q10", height=150)
        st.markdown("### Question 11")
        st.write("Have you ever had to give up something important for a bigger goal? What happened?")
        q11 = st.text_area("Your answer", key="q11", height=150)
        st.markdown("### Question 12")
        st.write("If someone told you that you couldn't achieve a goal you've set, how would you react and what would you do next?")
        q12 = st.text_area("Your answer", key="q12", height=150)
        st.session_state.responses.update({
            "q9": q9,
            "q10": q10,
            "q11": q11,
            "q12": q12
        })
        col1, col2 = st.columns(2)
        with col1:
            st.button("Previous", on_click=lambda: setattr(st.session_state, 'page', 3))
        with col2:
            st.button("Next", on_click=lambda: setattr(st.session_state, 'page', 5))
    
    elif st.session_state.page == 5:
        st.title("Section 4: Problem Solving and Learning")
        st.markdown("### Question 13")
        st.write("Looking back at last week, can you remember a time when you helped someone succeed? What did you do?")
        q13 = st.text_area("Your answer", key="q13", height=150)
        st.markdown("### Question 14")
        st.write("Can you share a time when you had to solve a problem using both your head and your heart? What did you do and what was the outcome?")
        q14 = st.text_area("Your answer", key="q14", height=150)
        st.markdown("### Question 15")
        st.write("How do you handle learning new things? What helps you understand and remember information?")
        q15 = st.text_area("Your answer", key="q15", height=150)
        st.markdown("### Question 16")
        st.write("How do you deal with feedback and criticism in your personal and professional life?")
        q16 = st.text_area("Your answer", key="q16", height=150)
        st.session_state.responses.update({
            "q13": q13,
            "q14": q14,
            "q15": q15,
            "q16": q16
        })
        col1, col2 = st.columns(2)
        with col1:
            st.button("Previous", on_click=lambda: setattr(st.session_state, 'page', 4))
        with col2:
            submit = st.button("Submit Survey")
            if submit:
                st.session_state.responses['unique_id'] = st.session_state.unique_id
                if save_response_db(st.session_state.responses):  # Save to SQLite database
                    st.session_state.page = 6
                    st.rerun()
    
    elif st.session_state.page == 6:
        st.title("Thank You!")
        st.markdown("""
        ## Your responses have been recorded.
        
        We appreciate your time and thoughtful answers. Your insights will be valuable for our research.
        
        If you'd like to take the survey again, you can click the reset button in the sidebar.
        """)
        # Display a download link for the data (admin only)
        if os.path.exists('survey_responses.db'):
            with st.expander("Admin Section (Download Data)"):
                st.write("This section is for administrators to download collected data.")
                admin_password = st.text_input("Admin Password", type="password")
                if admin_password == "admin123":
                    # For simplicity, we can export the entire database table as CSV using pandas.
                    conn = sqlite3.connect('survey_responses.db')
                    data = pd.read_sql_query("SELECT * FROM responses", conn)
                    conn.close()
                    st.dataframe(data)
                    csv = data.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name='all_survey_responses.csv',
                        mime='text/csv'
                    )

if __name__ == "__main__":
    main()
