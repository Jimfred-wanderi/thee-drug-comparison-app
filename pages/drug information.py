import streamlit as st
import pandas as pd

# Function to load Kaggle dataset
def load_dataset():
    # Load the Kaggle dataset
    df = pd.read_csv(r"C:\Users\User PC\thee-drug-comparison-app\kaggle\medicine_dataset.csv")
    return df[['name', 'sideEffect1', 'sideEffect2', 'sideEffect3', 'sideEffect4', 'Chemical Class']]

# Main function
def main():
    st.title("Drug Information Display")

    # Load dataset
    df = load_dataset()

    # Display search bar
    search_term = st.text_input("Search by Drug Name", "").strip().lower()

    # Filter dataset based on search term
    filtered_df = df[df['name'].str.lower().str.contains(search_term)]

    # Display search results
    if not filtered_df.empty:
        st.write("Search Results:")
        st.write(filtered_df)

        # Display details of selected drug
        selected_drug = st.selectbox("Select a Drug", filtered_df['name'].tolist())
        if selected_drug:
            details = filtered_df[filtered_df['name'] == selected_drug].iloc[0]
            st.write("Details about {}:".format(selected_drug))
            st.write("- Name: {}".format(details['name']))
            st.write("- Side Effect 1: {}".format(details['sideEffect1']))
            st.write("- Side Effect 2: {}".format(details['sideEffect2']))
            st.write("- Side Effect 3: {}".format(details['sideEffect3']))
            st.write("- Side Effect 4: {}".format(details['sideEffect4']))
            st.write("- Chemical Class: {}".format(details['Chemical Class']))
    else:
        st.write("No matching drugs found.")

if __name__ == "__main__":
    main()
