import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import mysql.connector

# Function to connect to MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Insert your MySQL password here
            database="drug and allergens"  # Replace with your database name
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

# Function to insert patient information into database
def insert_patient_info(conn, patient_name, patient_age, patient_gender, patient_allergies, prescriptions):
    try:
        cursor = conn.cursor()
        # Construct the SQL query
        sql = """
            INSERT INTO PatientInformation 
            (Name, Age, Gender, Allergies, Prescriptions)
            VALUES (%s, %s, %s, %s, %s)
        """
        # Convert prescriptions list to string
        prescriptions_str = ", ".join(prescriptions)
        # Execute the query
        cursor.execute(sql, (patient_name, patient_age, patient_gender, patient_allergies, prescriptions_str))
        # Commit the transaction
        conn.commit()
        return True
    except mysql.connector.Error as e:
        st.error(f"Error inserting patient information into database: {e}")
        return False

# Function to search inactive ingredients using Google
def search_inactive_ingredients_google(prescriptions):
    all_inactive_ingredients = []

    for prescription in prescriptions:
        # Construct the search query
        query = f"{prescription.strip()} inactive ingredients"

        # Send a search request to Google
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url)

        # Parse the HTML response
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            # Find all search results
            search_results = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
            # Initialize a list to store inactive ingredients for the current prescription
            inactive_ingredients = []
            # Iterate through search results
            for result in search_results:
                content = result.get_text()
                # Check if the content indicates relevant information about inactive ingredients
                if "inactive ingredients" in content.lower():
                    ingredients = extract_inactive_ingredients(content)
                    inactive_ingredients.extend(ingredients)
                    break  # Break after finding the first relevant result
            # Append the inactive ingredients for the current prescription to the combined list
            all_inactive_ingredients.append((prescription, inactive_ingredients))
        else:
            st.error(f"Failed to fetch search results for '{prescription}'. Please try again later.")

    return all_inactive_ingredients

# Function to extract inactive ingredients from content
def extract_inactive_ingredients(content):
    # Extract inactive ingredients from the content
    return [ingredient.strip() for ingredient in content.split("inactive ingredients:", 1)[-1].strip().split(",")]

# Function to load Kaggle dataset and generate substitutes
def generate_substitutes(prescription):
    # Load the Kaggle dataset
    df = pd.read_csv(r"C:\Users\User PC\thee-drug-comparison-app\kaggle\medicine_dataset.csv")

    # Filter substitutes for the given prescription
    substitutes = df.loc[df['name'].str.lower() == prescription.lower(), ['substitute0', 'substitute1', 'substitute2', 'substitute3']].values.flatten()
    
    # Filter out NaN values and convert to list
    substitutes = [sub for sub in substitutes if pd.notna(sub)]
    
    return substitutes

# Main function
def main():
    st.title("Patient Information Input")

    # Patient details input
    patient_name = st.text_input("Patient Name")
    patient_age = st.number_input("Patient Age", min_value=0, value=0, step=1)
    patient_gender = st.selectbox("Patient Gender", ["Male", "Female", "Other"])
    patient_allergies = st.text_input("Patient Allergies")

    # Prescription input
    num_prescriptions = st.number_input("Number of Prescriptions", min_value=1, value=1, step=1)
    prescriptions = []
    for i in range(num_prescriptions):
        prescription = st.text_input(f"Prescription {i+1}")
        prescriptions.append(prescription)

    # Button to find allergens
    if st.button("Find Allergens"):
        # Search for inactive ingredients using Google
        all_inactive_ingredients = search_inactive_ingredients_google(prescriptions)
        # Display the search results
        display_inactive_ingredients(all_inactive_ingredients)

        # Button to check for allergen match
        if len(prescriptions) > 0 and patient_allergies:
            allergen_match = check_allergen_match(patient_allergies, all_inactive_ingredients)
            if allergen_match:
                st.warning("Warning: The drugs prescribed contain allergens affecting the patient.")
            else:
                st.success("The drugs prescribed are safe to consume.")
    
    # Button to generate substitutes
    if st.button("Generate Substitutes"):
        for prescription in prescriptions:
            substitutes = generate_substitutes(prescription)
            if len(substitutes) > 0:
                st.write(f"Substitutes for {prescription}:")
                # Display substitutes in a table
                substitutes_df = pd.DataFrame({"Substitutes": substitutes})
                st.table(substitutes_df)
            else:
                st.write(f"No substitutes found for {prescription}.")

    # Button to save to database
    if st.button("Save to Database"):
        conn = connect_to_database()
        if conn is not None:
            if insert_patient_info(conn, patient_name, patient_age, patient_gender, patient_allergies, prescriptions):
                st.success("Patient information saved to database.")
            else:
                st.error("Failed to save patient information to database.")
            conn.close()

# Function to display inactive ingredients
def display_inactive_ingredients(all_inactive_ingredients):
    # Display the search results in point form
    st.subheader("Allergens")
    if all_inactive_ingredients:
        for prescription, inactive_ingredients in all_inactive_ingredients:
            st.write(f"Prescription: {prescription}")
            if inactive_ingredients:
                for ingredient in inactive_ingredients:
                    st.write(f"- {ingredient}")
            else:
                st.write("No inactive ingredients found.")
    else:
        st.write("No prescriptions provided.")

# Function to check allergen match
def check_allergen_match(patient_allergies, all_inactive_ingredients):
    # Check if patient's allergies match with any allergens from prescriptions
    if all_inactive_ingredients:
        patient_allergies_lower = patient_allergies.lower()
        for _, inactive_ingredients in all_inactive_ingredients:
            for ingredient in inactive_ingredients:
                if patient_allergies_lower in ingredient.lower():
                        return True  # Found a match
    return False

if __name__ == "__main__":
    main()
