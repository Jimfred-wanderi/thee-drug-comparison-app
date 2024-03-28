import streamlit as st
import mysql.connector

# Function to connect to MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",  # Insert your MySQL password here
            database="drug and allergens"  # Corrected database name
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None

# Function to authenticate user
def authenticate(username, password):
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return True
    return False

# Main login page
def login_page():
    st.title("Log In")
    username = st.text_input("Username", key="login_username_input")
    password = st.text_input("Password", type="password", key="login_password_input")
    if st.button("Log In"):
        if authenticate(username, password):
            st.session_state.logged_in = True  # Initialize logged_in attribute
            st.success("Logged in successfully!")
            # Store user session here (e.g., set a session token)
            st.write("Redirecting...")
            st.experimental_rerun()  # Rerun the app to redirect automatically
        else:
            st.error("Invalid username or password.")

# Allergen checker page
def patient_page():
    st.title("patient page")
    st.write("Welcome to the patient page!")

# Main function
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Initialize logged_in attribute if not exists
    # Check if the user is logged in (use session management)
    if st.session_state.logged_in:
        patient_page()  # Display the allergen checker page if logged in
    else:
        login_page()

if __name__ == "__main__":
    main()
