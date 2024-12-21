import json
import time
import random
from tqdm import tqdm  # You can install tqdm for progress bars using pip: pip install tqdm
from gemini import get_response  # Replace with actual import

# Function to fill JSON answers with batching and retry logic, including progress tracking
def fill_json_answers(input_json_path, batch_size=10, retry_attempts=3, retry_delay=2):
    # Load the JSON file with questions
    with open(input_json_path, 'r', encoding='utf-8') as json_file:
        questions_data = json.load(json_file)

    # Check if the JSON structure is a dictionary (which it is)
    if isinstance(questions_data, dict):
        print("The JSON data is a dictionary. Processing each category...")

        # Loop through each category ('Conceptual', 'Mathematical', 'Descriptive')
        for category, questions_list in questions_data.items():
            print(f"Processing category: {category} with {len(questions_list)} questions...")

            total_questions = len(questions_list)
            
            # Process questions in batches
            for i in tqdm(range(0, total_questions, batch_size), desc=f"Processing Batches ({category})", unit="batch"):
                batch = questions_list[i:i + batch_size]  # Get a batch of questions
                batch_number = i // batch_size + 1  # Keep track of batch number

                print(f"\nProcessing batch {batch_number} of category {category} with {len(batch)} questions...")

                for index, entry in enumerate(batch):
                    question = entry.get('question')  # Access the question
                    attempts = 0

                    while attempts < retry_attempts:
                        try:
                            # Get the answer from the chatbot
                            answer = get_response(question)
                            
                            # Add the answer to the entry
                            entry['answer'] = answer

                            # Simulate delay to avoid hitting API limits
                            time.sleep(random.uniform(1, 3))  # Random delay between 1-3 seconds
                            
                            print(f"Question {i + index + 1}/{total_questions} in {category} answered successfully.")
                            break  # Exit the retry loop if successful

                        except Exception as e:
                            print(f"Error processing question {i + index + 1} in {category}: {question}, Attempt {attempts + 1}, Error: {str(e)}")
                            attempts += 1
                            time.sleep(retry_delay)  # Wait before retrying

                    if attempts == retry_attempts:
                        print(f"Failed to process question {i + index + 1} in {category} after {retry_attempts} attempts.")

    # Save the updated JSON data back to the file
    with open(input_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(questions_data, json_file, ensure_ascii=False, indent=4)

    print(f"Answers have been filled and saved to {input_json_path}")

# Example usage
for i in range(7, 9):
    print(f"Filling answers for questions in answer{i}.json...")
    input_json_path = f"D:\\Codes\\cse299phychatbot\\answersort\\answer{i}.json"  # Replace with your input JSON file path

    # Process the JSON file with a batch size of 10 and track progress
    fill_json_answers(input_json_path, batch_size=10, retry_attempts=3, retry_delay=2)
    print(f"All questions in answer{i}.json processed successfully.")
    i = i+1
