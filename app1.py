from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import openai
from dotenv import load_dotenv
import random

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Load environment variables securely
load_dotenv()

# Set the OpenAI API key from the environment variables
openai.api_key = os.getenv('OPEN_AI_KEY')

def fetch_census_data():
    """Fetches census data from an API and returns it as a string."""
    api_url = "https://api.census.gov/data/2020/dec/pl?get=P1_001N&for=state:72"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises exception for 4XX or 5XX errors
        data = response.json()
        print("Census data fetched successfully:", data)  # Debug print
        return str(data)
    except requests.RequestException as e:
        error_msg = f"Failed to fetch data due to an error: {e}"
        print(error_msg)  # Debug print
        return error_msg

def get_openai_response(prompt_text):
    """Gets a response from OpenAI's chat model with a given prompt text."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_text}]
        )
        original_response = response.choices[0].message['content'].strip()
        print("OpenAI response:", original_response)  # Debug print
        personalized_response = personalize_response(original_response)
        return personalized_response
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(error_msg)  # Debug print
        return error_msg

def personalize_response(response_text):
    """Modifies the response to add a unique personality touch."""
    snobby_additions = [
        "Well, of course, that's the only sensible option.",
        "I suppose you wouldn't know, but it's quite elementary.",
        "Ah, finally, a question worth my time."
    ]
    personalized_text = f"{response_text} {random.choice(snobby_additions)}"
    print("Personalized response:", personalized_text)  # Debug print
    return personalized_text

@app.route('/chat', methods=['POST'])
@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint for chatting with the OpenAI model, including fetched census data."""
    data = request.get_json()
    prompt_text = data.get('message').strip().lower()  # Normalize the input to handle variations like "Hello", "hello", etc.

    # Check if the message is "hello"
    if prompt_text == "hello":
        # Directly return a greeting response without fetching census data or contacting OpenAI
        return jsonify({"response": "Hello there! How can I assist you today?"})

    # If the message is not "hello", proceed as before
    census_data = fetch_census_data()
    # Example for formatting census data directly, adjust based on your actual data structure
    # This is a placeholder; you'll need to adapt it based on the actual response structure and requirements
    population_info = "The latest census data might be interesting. Let's discuss that."
    full_prompt = f"{prompt_text}\n\nDid you know? {population_info}\nHow might this information be important?"

    response_text = get_openai_response(full_prompt)
    return jsonify({"response": response_text})


if __name__ == '__main__':
    app.run(debug=True)
