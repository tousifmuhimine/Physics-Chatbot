import json
import time
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core.exceptions import ResourceExhausted

# Initialize the Gemini model (replace with your actual API key)
API_KEY = "AIzaSyCvj3WDqsOS0nYtznSMZ2fgjjrDsS8Z8AM"
gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=API_KEY)

# Define a template for the prompt
template = """
You are an expert in physics, and your task is to compare the provided answers to a given question. Below, I have provided a question, an actual correct answer, and a generated answer. Your job is to rate how accurate the generated answer is in response to the question, considering how similar it is to the actual correct answer, while also ensuring it addresses the question correctly.

Please provide an **accuracy score** between **0.0** and **1.0**, where:
- **0.0** means the generated answer does not correctly answer the question.
- **1.0** means the generated answer is perfectly accurate in addressing the question.

Here is the information:

**Question**:
{question}

**Actual Correct Answer**:
{actual_answer}

**Generated Answer**:
{generated_answer}

Please provide only the accuracy score between 0.0 and 1.0.
"""

# Function to evaluate the accuracy of a generated answer using the Gemini model
def evaluate_answer_accuracy(question, actual_answer, generated_answer):
    time.sleep(1)  # Add a delay to avoid hitting API limits
    
    # Format the prompt with the question, actual, and generated answers
    prompt = template.format(question=question, actual_answer=actual_answer, generated_answer=generated_answer)
    
    try:
        # Invoke the Gemini model and get the response
        response = gemini_model.invoke(prompt)
        
        # Extract the accuracy score directly from the response
        accuracy_score = float(response.content.strip())  # Directly extract the numeric score
        return accuracy_score
    except ResourceExhausted:
        print("API quota exhausted. Assigning 0.5 as the accuracy score.")
        return 0.5  # Assign 0.5 if the quota is exhausted
    except ValueError as e:
        print(f"Error extracting accuracy score: {e}")
        return 0

# Load both JSON files (actual answers and generated answers)
with open('actual_answers/answer7.json', 'r', encoding='utf-8') as f:
    actual_data = json.load(f)
with open('test_answers/test7.json', 'r', encoding='utf-8') as f:
    generated_data = json.load(f)

# Initialize counters for precision, recall, and F1 score calculation
total_answers = 0
accurate_answers = 0  # For precision (accuracy >= 0.5)
high_accuracy_answers = 0  # For recall (accuracy >= 0.8)

# Initialize a list to store accuracy outputs for saving to the txt file
accuracy_outputs = []

# Function to calculate the average accuracy for a sector and print accuracy for each question
def calculate_sector_metrics(sector):
    total_accuracy = 0
    count = 0
    global accurate_answers, high_accuracy_answers, total_answers
    for actual, generated in zip(actual_data[sector], generated_data[sector]):
        question = actual['question']
        actual_answer = actual['answer']
        generated_answer = generated['answer']
        accuracy = evaluate_answer_accuracy(question, actual_answer, generated_answer)
        total_accuracy += accuracy
        count += 1
        total_answers += 1
        
        if accuracy >= 0.5:
            accurate_answers += 1  # Count for precision
        if accuracy >= 0.8:
            high_accuracy_answers += 1  # Count for recall
        
        # Print accuracy for each question
        print(f"Question: {question}")
        print(f"Accuracy: {accuracy:.2f}")
    
    return total_accuracy / count if count > 0 else 0

# Calculate metrics for each sector
sectors = ['Conceptual', 'Mathematical', 'Descriptive']
sector_accuracies = {}
sector_precisions = {}
sector_recalls = {}
sector_f1_scores = {}

for sector in sectors:
    sector_accuracy = calculate_sector_metrics(sector)
    sector_accuracies[sector] = sector_accuracy

    # Precision for the sector (answers with accuracy >= 0.5 are considered "correct")
    precision = accurate_answers / total_answers if total_answers > 0 else 0
    sector_precisions[sector] = precision

    # Recall for the sector (answers with accuracy >= 0.8 are considered "highly correct")
    recall = high_accuracy_answers / total_answers if total_answers > 0 else 0
    sector_recalls[sector] = recall

    # F1 score for the sector
    if precision + recall > 0:
        f1_score = 2 * (precision * recall) / (precision + recall)
    else:
        f1_score = 0
    sector_f1_scores[sector] = f1_score

    # Save metrics for this sector to the output
    accuracy_outputs.append(f"Average Accuracy for {sector}: {sector_accuracy:.2f}\n")
    accuracy_outputs.append(f"Precision for {sector}: {precision:.2f}\n")
    accuracy_outputs.append(f"Recall for {sector}: {recall:.2f}\n")
    accuracy_outputs.append(f"F1 Score for {sector}: {f1_score:.2f}\n")

# Calculate overall metrics (accuracy, precision, recall, F1 score) across all sectors
overall_accuracy = sum(sector_accuracies.values()) / len(sector_accuracies)
overall_precision = sum(sector_precisions.values()) / len(sector_precisions)
overall_recall = sum(sector_recalls.values()) / len(sector_recalls)

if overall_precision + overall_recall > 0:
    overall_f1_score = 2 * (overall_precision * overall_recall) / (overall_precision + overall_recall)
else:
    overall_f1_score = 0

# Add overall metrics to the output
accuracy_outputs.append(f"Total Average Accuracy: {overall_accuracy:.2f}\n")
accuracy_outputs.append(f"Total Precision: {overall_precision:.2f}\n")
accuracy_outputs.append(f"Total Recall: {overall_recall:.2f}\n")
accuracy_outputs.append(f"Total F1 Score: {overall_f1_score:.2f}\n")

# Create the accuracy folder if it doesn't exist
if not os.path.exists('accuracy'):
    os.makedirs('accuracy')

# Save the final metrics to the accuracy1.txt file
with open('accuracy/accuracy7.txt', 'w', encoding='utf-8') as f:
    f.writelines(accuracy_outputs)
