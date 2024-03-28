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
            st.session_state.logged_in = True  # Set session state to indicate logged in
            st.success("Logged in successfully!")  # Display success message
            # Store user session here (e.g., set a session token)
            st.write("Redirecting to dashboard...")
            st.experimental_rerun()  # Rerun the app to redirect automatically
        else:
            st.error("Invalid username or password.")

# Restricted page accessible only to logged-in users
def restricted_page():
    st.title("Restricted Page")
    st.write("This page is restricted. You need to log in to access it.")
    if st.button("Log In"):
        login_page()

# Main function
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # Initialize logged_in attribute if not exists
    if st.session_state.logged_in:
        st.write("Welcome! You are logged in.")
        # Render restricted page
        restricted_page()
    else:
        # Render login page
        login_page()

if __name__ == "__main__":
    main()
