import json
# from chatbot import get_response  # Import the get_response function from chatbot.py
from gemini import get_response  # Import the get_response function from gemini.py

def fill_json_answers(input_json_path):
    # Load the JSON file with questions
    with open(input_json_path, 'r', encoding='utf-8') as json_file:
        questions_data = json.load(json_file)

    # Process each question to get the response from the chatbot
    for entry in questions_data:
        question = entry['question']

        # Get the answer from the chatbot
        answer = get_response(question)

        # Fill the answer slot in the JSON data
        entry['answer'] = answer

    # Save the updated JSON data back to the file
    with open(input_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(questions_data, json_file, ensure_ascii=False, indent=4)

    print(f"Answers have been filled and saved to {input_json_path}")

# Specify the path to your input JSON file
for i in range(1, 2):
    input_json_path = f"D:\\Codes\\cse299phychatbot\\p.json"
    # Run the function
    print(f"Filling answers for {i}...")
    fill_json_answers(input_json_path)
    print(f"Done {i}!")
    i = i+1

# input_json_path = "D:\\Codes\\cse299phychatbot\\p.json"
# # Run the function
# print(f"Filling answers for 1...")
# fill_json_answers(input_json_path)
# print(f"Done 1!")
 

