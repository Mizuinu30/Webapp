import os
import openai
from dotenv import load_dotenv
import random

load_dotenv()

# Assuming you have the OpenAI API key
openai.api_key = os.getenv('OPEN_AI_KEY')

def get_openai_response(prompt_text):
    """
    Function to get a response from OpenAI's chat model, with personality.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt_text}
            ]
        )
        original_response = response.choices[0].message['content'].strip()
        # Post-process the response to inject personality
        personalized_response = personalize_response(original_response)
        return personalized_response
    except Exception as e:
        return f"An error occurred: {str(e)}"

def personalize_response(response_text):
    """
    Modify the response to reflect the chatbot's snobby personality.
    """
    # Example: Adding a touch of snobbery to the response
    snobby_additions = [
        "Well, of course, that's the only sensible option.",
        "I suppose you wouldn't know, but it's quite elementary.",
        "Ah, finally, a question worth my time."
    ]
    # Add a random snobby phrase to the response
    return f"{response_text} {random.choice(snobby_additions)}"


if __name__ == "__main__":
    while True:
        prompt_text = input("Please enter your question (or type 'exit' to quit): ")
        if prompt_text.lower() == 'exit':
            print("Exiting. Have a great day!")
            break
        response_text = get_openai_response(prompt_text)
        print(response_text)
