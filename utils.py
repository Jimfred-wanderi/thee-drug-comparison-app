import requests
import pandas as pd
from bs4 import BeautifulSoup

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
            print(f"Failed to fetch search results for '{prescription}'. Please try again later.")

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

# Function to display inactive ingredients
def display_inactive_ingredients(all_inactive_ingredients):
    # Display the search results in point form
    print("Allergens")
    if all_inactive_ingredients:
        for prescription, inactive_ingredients in all_inactive_ingredients:
            print(f"Prescription: {prescription}")
            if inactive_ingredients:
                for ingredient in inactive_ingredients:
                    print(f"- {ingredient}")
            else:
                print("No inactive ingredients found.")
    else:
        print("No prescriptions provided.")

# Function to check allergen match
def check_allergen_match(patient_allergies, all_inactive_ingredients):
    # Check if patient's allergies match with any allergens from prescriptions
    if all_inactive_ingredients:
        patient_allergies_lower = patient_allergies.lower()
        for _, inactive_ingredients in all_inactive_ingredients:
            for ingredient in inactive_ingredients:
                if patient_allergies_lower in ingredient.lower():
                    return True
    return False
