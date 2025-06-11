import streamlit as st
import json
from pathlib import Path

# Use Streamlit's cache to avoid reloading data on every user interaction.
@st.cache_data
def load_json(file_path):
    """Safely loads a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found. Please make sure it exists.")
        return None
    except json.JSONDecodeError:
        st.error(f"Error: The file '{file_path}' is not a valid JSON file.")
        return None

def load_app_data():
    """Loads all necessary data for the app."""
    symptom_data = load_json("symptom_to_muscle_master.json")
    muscle_images = load_json("muscle_to_image.json")
    return symptom_data, muscle_images