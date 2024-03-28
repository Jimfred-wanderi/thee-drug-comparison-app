import streamlit as st

# Function to authenticate user
def authenticate_user(username, password):
    # Replace this logic with your actual authentication mechanism
    return username == "admin" and password == "password"

# Function to render the login page
def login_page():
    st.title("Log In")
    username = st.text_input("Username", key="login_username_input")
    password = st.text_input("Password", type="password", key="login_password_input")
    if st.button("Log In"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True  # Set session state to indicate logged in
            st.success("Logged in successfully!")  # Display success message
            st.experimental_rerun()  # Reload the app to render the homepage
        else:
            st.error("Invalid username or password.")
    
    st.write("Don't have an account? Sign up now!")
    if st.button("Sign Up"):
        st.experimental_rerun()  # Reload the app to render sign-up page

# Function to render the homepage content
def homepage_content():
    st.title("Welcome to the Homepage")
    st.write("You are now logged in.")

# Main function
def main():
    if not st.session_state.get("logged_in"):
        st.session_state.logged_in = False  # Initialize logged_in attribute if not exists

    if st.session_state.logged_in:
        homepage_content()  # Render original homepage content
    else:
        login_page()  # Render login page

if __name__ == "__main__":
    main()
