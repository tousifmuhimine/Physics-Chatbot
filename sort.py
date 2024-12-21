import json

# Function to categorize a question based on its content
def categorize_question(question):
    question = question.lower()
    
    # Categorization logic based on keywords
    if any(keyword in question for keyword in ["calculate", "find", "determine", "value", "formula"]):
        return "Mathematical"
    elif any(keyword in question for keyword in ["describe", "explain", "summarize", "elaborate", "definition", "what is"]):
        return "Descriptive"
    else:
        return "Conceptual"

# Function to load the JSON file, categorize, and save the output
def process_json_file(input_json_path, output_json_path):
    # Load the JSON file with questions
    with open(input_json_path, 'r', encoding='utf-8') as json_file:
        questions_data = json.load(json_file)

    # Initialize the categorized questions dictionary
    categorized_questions = {
        "Conceptual": [],
        "Mathematical": [],
        "Descriptive": []
    }

    # Process each question to categorize it
    for entry in questions_data:
        question = entry['question']

        # Categorize the question
        category = categorize_question(question)

        # Append the question to the appropriate category
        categorized_questions[category].append({
            "question": question,
            "answer": entry.get('answer', '')  # Retain the existing answers if they are already present
        })

    # Save the categorized questions into a new JSON file
    with open(output_json_path, 'w', encoding='utf-8') as output_file:
        json.dump(categorized_questions, output_file, ensure_ascii=False, indent=4)

    print(f"Categorized questions saved to {output_json_path}")

# Example usage
for i in range(2, 3):
    input_json_path = f"D:\\Codes\\cse299phychatbot\\actual_answers\\answer{i}.json"  # Replace with your input JSON file path
    output_json_path = f"D:\\Codes\\cse299phychatbot\\answersort\\answer{i}.json"  # Replace with your output JSON file path

    process_json_file(input_json_path, output_json_path)
    i = i+1


process_json_file(input_json_path, output_json_path)
