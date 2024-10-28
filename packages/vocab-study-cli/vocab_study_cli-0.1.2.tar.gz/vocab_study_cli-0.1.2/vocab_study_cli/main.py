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
        # English word definition for Japanese learners with examples and Japanese translation
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": f"Explain the English word '{word}' in simple terms for a Japanese learner. "
                           "Provide a brief definition in English, an example sentence, a Japanese translation, "
                           "and, if possible, synonyms and antonyms."
            }]
        )
        definition = response.choices[0].message.content
        return definition.strip()
    except Exception as e:
        return f"Error retrieving definition: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="A CLI tool for Japanese learners to study English vocabulary using OpenAI API.")
    parser.add_argument("word", type=str, help="The English word to look up.")
    args = parser.parse_args()
    definition = get_word_definition(args.word)
    print(f"Definition of '{args.word}':\n{definition}")

if __name__ == "__main__":
    main()
