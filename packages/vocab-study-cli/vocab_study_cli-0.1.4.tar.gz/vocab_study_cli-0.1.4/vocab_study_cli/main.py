import os
import json
from dotenv import load_dotenv
import anthropic
import argparse

# Load environment variables
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Instantiate the Anthropic client
client = anthropic.Anthropic(api_key=api_key)

def get_word_info(word):
    # Define the system message to provide context for the assistant's role
    system_message = (
        "You are an assistant providing comprehensive vocabulary information for Japanese English learners. "
        "Generate JSON data for the word with the following fields strictly in JSON format: "
        "{word, ipa, meanJP, typeOfWord (ex: verb: EN, JP), cefr, frequency (highest, high, often, rare), "
        "define [EN, JP], origin [EN, JP], formality [EN, JP], "
        "usage [Contextual Usage: Describe situations where this word is suitable or not in both EN and JP, "
        "Decision Factors: Criteria for choosing this word over others in both EN and JP, "
        "Examples: Provide real-life examples with explanations of meaning and intent in both EN and JP], "
        "exampleSentence [EN, JP], exampleArticles [EN, JP], exampleTalks [EN, JP], exampleToddler [EN, JP], "
        "collocation1..3 [EN, JP, sample<EN, JP>], idiom1..3 [EN, JP, sample<EN, JP>], "
        "slang1..3 [EN, JP, sample<EN, JP>], alternative1..3 [EN, JP, sample<EN, JP>], "
        "synonyms1..3 [item, differ, sample<EN, JP>], antonym1..3 [item, differ, sample<EN, JP>], "
        "note [EN, JP], SpeechChanges (if exist, or 'na'): EN, JP}. "
        "Do not add any text outside of this JSON object."
    )
    
    # Messages to request specific JSON data for the word
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Generate JSON data from word: '{word}'."
                }
            ]
        }
    ]

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            temperature=1,
            system=system_message,
            messages=messages
        )
        
        # Extract and parse the JSON response
        word_info = response.content[0].text.strip()
        
        # Attempt to parse the response as JSON
        word_info_json = json.loads(word_info)
        return word_info_json

    except json.JSONDecodeError:
        print("Error: Unable to parse response as JSON. Here is the raw response:")
        print(word_info)
        return {"error": "Failed to parse response as JSON", "response": word_info}
    except Exception as e:
        return {"error": f"Error retrieving word information: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description="A CLI tool for Japanese learners to study English vocabulary using Anthropic API.")
    parser.add_argument("word", type=str, help="The English word to look up.")
    args = parser.parse_args()
    word_info = get_word_info(args.word)
    print(json.dumps(word_info, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
