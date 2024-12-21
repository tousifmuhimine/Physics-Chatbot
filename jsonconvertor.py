from docx import Document
import json

def extract_questions_to_json(docx_path, json_path):
    # Load the document
    doc = Document(docx_path)
    
    # Initialize a list to hold questions
    questions_list = []
    
    # Loop through each paragraph in the document
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:  # Ensure the text is not empty
            # Create a dictionary in the specified format
            question_obj = {
                "question": text,
                "answer": ""
            }
            questions_list.append(question_obj)
    
    # Write the list to a JSON file
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(questions_list, json_file, ensure_ascii=False, indent=4)

# Specify the path to the docx file and output json file
docx_path = "C:/Users/User/Desktop/j/ch13.docx"

json_path = "C:/Users/User/Desktop/j/tousif/ch13.json"

# Call the function
extract_questions_to_json(docx_path, json_path)

print(f"Questions have been extracted and saved to {json_path}")