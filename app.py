import streamlit as st
from data_loader import load_app_data
from symptom_analyzer import get_symptom_key_from_gpt, generate_conversational_response
from ui_components import display_results

# --- Page Configuration ---
st.set_page_config(
    page_title="AI-Powered Pain & Muscle Assistant for Low Back Pain",
    page_icon="💪",
    layout="wide"
)

# --- Main Application ---
st.title("🤖 AI-Powered Pain & Muscle Assistant for Low Back Pain")
st.markdown("Describe your pain, and this AI assistant will identify potential muscular sources based on common trigger point referral patterns.")

# --- Load Data ---
symptom_data, muscle_image_map = load_app_data()

# Check if data loaded correctly before proceeding
if symptom_data and muscle_image_map:
    
    # --- Check for API Key ---
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except KeyError:
        st.error("OpenAI API key not found. Please add it to your `.streamlit/secrets.toml` file.")
        st.stop()

    # --- User Input ---
    user_input = st.text_area(
        "Please describe your pain in detail (e.g., location, type of pain, what makes it worse):",
        height=100,
        placeholder="e.g., I get a sharp pain in my lower right back when I stand up, and it sometimes aches deep in my buttock."
    )

    if st.button("Analyze My Symptoms", type="primary"):
        if not user_input.strip():
            st.warning("Please enter a description of your symptoms.")
        else:
            with st.spinner("🧠 AI is analyzing your symptoms... Please wait."):
                
                # 1. Use GPT-4 to map input to a known symptom key
                symptom_keys = list(symptom_data.keys())
                matched_key = get_symptom_key_from_gpt(user_input, symptom_keys, api_key)

                if matched_key and matched_key != "None":
                    st.success(f"Analysis complete! Matched to symptom: **{matched_key}**")
                    
                    # 2. Get the data for the matched symptom
                    symptom_details = symptom_data.get(matched_key, {})
                    muscles = symptom_details.get("muscles", [])
                    
                    if muscles:
                        # 3. Generate a conversational opening
                        conversational_text = generate_conversational_response(user_input, matched_key, muscles, api_key)
                        st.markdown(conversational_text)
                        
                        # 4. Display the results (muscles and images)
                        display_results(muscles, muscle_image_map)
                    else:
                        st.error(f"A match was found for '{matched_key}', but no muscles are listed for it in the database.")

                else:
                    st.error("I couldn't confidently match your description to a known symptom in the database. Please try describing your pain with more detail or in a different way.")

# Add a footer
st.markdown("---")
st.markdown("*Disclaimer: This tool is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.*")