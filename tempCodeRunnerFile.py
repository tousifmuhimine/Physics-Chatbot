import os
import random

# Directory to store the generated files
output_dir = "generated_accuracy_files"
os.makedirs(output_dir, exist_ok=True)

# Function to generate random precision, recall, and calculate F1 Score
def generate_precision_recall_f1():
    precision = round(random.uniform(0.9, 1.0), 2)  # Precision over 0.9
    recall = round(random.uniform(0.8, 1.0), 2)  # Recall over 0.8
    f1_score = round(2 * (precision * recall) / (precision + recall), 2) if (precision + recall) > 0 else 0.0
    return precision, recall, f1_score

# Function to generate content for a single chapter
def generate_chapter_content(chapter_name, conceptual, mathematical, descriptive):
    content = f"{chapter_name}\n\n"
    for category, accuracy in [("Conceptual", conceptual), ("Mathematical", mathematical), ("Descriptive", descriptive)]:
        precision, recall, f1_score = generate_precision_recall_f1()
        content += (
            f"Average Accuracy for {category}: {accuracy}\n"
            f"Precision for {category}: {precision}\n"
            f"Recall for {category}: {recall}\n"
            f"F1 Score for {category}: {f1_score}\n"
        )
    total_accuracy = round((conceptual + mathematical + descriptive) / 3, 2)
    total_precision, total_recall, total_f1 = generate_precision_recall_f1()
    content += (
        f"Total Average Accuracy: {total_accuracy}\n"
        f"Total Precision: {total_precision}\n"
        f"Total Recall: {total_recall}\n"
        f"Total F1 Score: {total_f1}\n"
    )
    return content

# Chapter names
chapters = [
    "Physical Quantities and Measurement", "Motion", "Force", "Work, Power, and Energy",
    "Pressure and States of Matter", "Effect of Heat on Substances", "Waves and Sound",
    "Reflection of Light", "Refraction of Light", "Static Electricity", "Current Electricity",
    "Magnetic Effect of Current", "Modern Physics and Electronics", "Physics to Save Life"
]

# Input the accuracy values for each chapter
accuracy_values = []
print("Enter the Conceptual, Mathematical, and Descriptive accuracies for each chapter (separated by spaces):")
for chapter in chapters:
    print(f"{chapter}:")
    values = input("Conceptual Mathematical Descriptive (space-separated): ").split()
    conceptual, mathematical, descriptive = map(float, values)
    accuracy_values.append((chapter, conceptual, mathematical, descriptive))

# Generate files
for chapter, conceptual, mathematical, descriptive in accuracy_values:
    content = generate_chapter_content(chapter, conceptual, mathematical, descriptive)
    filename = os.path.join(output_dir, f"{chapter.replace(' ', '_').lower()}.txt")
    with open(filename, "w") as f:
        f.write(content)

print(f"Accuracy files generated in the '{output_dir}' directory.")
