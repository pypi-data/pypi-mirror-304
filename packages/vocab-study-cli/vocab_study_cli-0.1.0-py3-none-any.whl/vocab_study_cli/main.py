# vocab_study_cli/main.py

from openai import OpenAI
import os
from dotenv import load_dotenv
import argparse

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Instantiate the OpenAI client
client = OpenAI(api_key=api_key)

def get_word_definition(word):
    try:
        # Using the chat completion API in the new client format
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Define the word '{word}' for a language learner."}]
        )
        definition = response.choices[0].message.content
        return definition.strip()
    except Exception as e:
        return f"Error retrieving definition: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="A CLI tool for learning vocabulary using OpenAI API.")
    parser.add_argument("word", type=str, help="The word to look up.")
    args = parser.parse_args()
    definition = get_word_definition(args.word)
    print(f"Definition of {args.word}: {definition}")

if __name__ == "__main__":
    main()
