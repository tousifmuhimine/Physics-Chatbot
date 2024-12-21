import json
import glob
from collections import defaultdict

def merge_json_files(folder_path, output_file):
    # Dictionary to hold merged data by category
    merged_data = defaultdict(list)

    # Load all JSON files in the folder
    for file_path in glob.glob(f"{folder_path}/answer*.json"):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Merge data into the corresponding category
            for category, qa_list in data.items():
                merged_data[category].extend(qa_list)

    # Save the merged data to a new JSON file
    with open(output_file, "w", encoding="utf-8") as output:
        json.dump(merged_data, output, indent=4)

    print(f"Merged data saved to {output_file}")

# Folder containing the JSON files
folder_path = "actual_answers"  # Replace with your folder name
output_file = "merged_answers.json"  # Output file name

# Call the function to merge files
merge_json_files(folder_path, output_file)
