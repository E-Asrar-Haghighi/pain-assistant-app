import streamlit as st
from pathlib import Path

def display_results(muscles, muscle_to_image_map):
    """
    Renders the list of muscles and their corresponding diagrams in the UI.
    """
    if not muscles:
        st.info("No specific muscles were found for this symptom in our database.")
        return

    st.subheader("Potential Muscle Sources and Their Referral Patterns")

    for muscle in muscles:
        st.markdown(f"---")
        st.markdown(f"#### {muscle}")

        image_path = muscle_to_image_map.get(muscle)

        if image_path and Path(image_path).exists():
            st.image(image_path, caption=f"Typical pain referral pattern for the {muscle}.")
        else:
            st.warning(f"No diagram available for **{muscle}** in the database.")