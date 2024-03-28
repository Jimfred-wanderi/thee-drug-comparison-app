import streamlit as st
import random
import mysql.connector

# Function to generate a random OTP
def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

# Placeholder function to send OTP to the user's phone number
def send_otp(phone_number, otp):
    # Code to send OTP to the provided phone number via SMS
    # This could be done using a third-party SMS API or a service provider
    # For demonstration purposes, we'll just print the OTP here
    print(f"OTP sent to {phone_number}: {otp}")
    return otp  # Return the generated OTP

# Function to connect to MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",  # Insert your MySQL password here
            database="drug_and_allergens"  # Corrected database name
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL database:", e)
        return None

# Function to insert user details into MySQL database
def insert_user(conn, user_data):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, phone_number, username, password)
            VALUES (%s, %s, %s, %s, %s)
        """, user_data)
        conn.commit()
        return True
    except mysql.connector.Error as e:
        print("Error inserting user into database:", e)
        return False

def signup_page():
    st.title("Welcome to Drug and Allergens Signup Page")
    st.markdown("![Welcome Banner](https://example.com/welcome_banner.png)")
    st.write("Please fill out the following details to sign up.")

    # Input fields with unique keys
    name = st.text_input("Full Name", key="full_name_input")
    email = st.text_input("Email", key="email_input")
    phone_number = st.text_input("Phone Number", key="phone_number_input")
    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password_input")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Save user details to database (or any other data store)
            conn = connect_to_database()
            if conn is not None:
                user_data = (name, email, phone_number, username, password)
                if insert_user(conn, user_data):
                    # Generate OTP
                    otp = generate_otp()
                    # Send OTP to the user's phone number
                    sent_otp = send_otp(phone_number, otp)
                    st.success("Sign up successful! Please check your phone for the OTP.")
                    # Prompt user to enter OTP
                    user_entered_otp = st.text_input("Enter OTP")
                    if user_entered_otp == sent_otp:
                        st.success("OTP verified.")
                        st.experimental_rerun()  # Rerun the app to redirect to login page
                    else:
                        st.error("Invalid OTP. Please try again.")
                else:
                    st.error("Failed to sign up. Please try again.")
                conn.close()

if __name__ == "__main__":
    signup_page()
