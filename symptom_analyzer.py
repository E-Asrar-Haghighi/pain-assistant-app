import openai

def get_symptom_key_from_gpt(user_input, symptom_keys, api_key):
    """
    Uses GPT-4o-mini to map a user's free-text description to a predefined symptom key.
    """
    openai.api_key = api_key
    
    system_prompt = """
    You are an expert medical assistant. Your task is to analyze a user's description of their pain
    and match it to the single most relevant symptom key from a provided list.
    Respond with ONLY the matching key from the list. Do not add any explanation or pleasantries.
    If no key is a clear match, respond with the word 'None'.
    """

    user_prompt = f"""
    Here is the list of available symptom keys:
    {symptom_keys}

    Here is the user's pain description:
    "{user_input}"

    Based on the user's description, which is the single most relevant key from the list?
    """
    
    try:
        response = openai.chat.completions.create(
            # --- CHANGE HERE ---
            model="gpt-4o-mini", # Using the faster, cheaper model
            # -------------------
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=50
        )
        matched_key = response.choices[0].message.content.strip().strip('"')
        return matched_key
    except Exception as e:
        print(f"An OpenAI API error occurred: {e}")
        return None

def generate_conversational_response(user_input, matched_symptom, muscles, api_key):
    """
    Generates a natural, human-like response explaining the findings using GPT-4o-mini.
    """
    openai.api_key = api_key

    system_prompt = """
    You are an empathetic and helpful AI health assistant. Your role is to explain potential
    muscular sources of pain to a user in a clear, conversational, and reassuring way.
    Do not give medical advice. Frame your response as informational, based on common
    pain referral patterns.
    """

    user_prompt = f"""
    A user described their pain as: "{user_input}"

    Our system matched this to the symptom pattern: "{matched_symptom}"

    The muscles commonly associated with this pattern are: {', '.join(muscles)}.

    Please write a brief, conversational response (2-3 sentences) that I can show to the user.
    It should confirm what you've understood and introduce the potential muscle connections.
    For example: "Based on your description of..., it sounds like you're experiencing symptoms
    often linked to... The muscles that are commonly involved include... You can see their
    typical pain patterns below."
    """

    try:
        response = openai.chat.completions.create(
            # --- CHANGE HERE ---
            model="gpt-4o-mini", # Using the faster, cheaper model
            # -------------------
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An OpenAI API error occurred: {e}")
        return "There was an error generating a response. Please check the logs."