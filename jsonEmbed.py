import os
import json
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Initialize embeddings
embeddings = OllamaEmbeddings(model="all-minilm:33m")

# Set up directories
current_directory = os.path.dirname(os.path.abspath(__file__))
vector_directory = os.path.join(current_directory, "db", "chroma_db_json")


def load_json_data(json_file_path):
    """Load data from the JSON file."""
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"The file {json_file_path} does not exist.")
    
    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    questions = []
    answers = []

    for category, items in data.items():
        for item in items:
            questions.append(item["question"])
            answers.append(item["answer"])
    
    return questions, answers


def store_in_vector_store(questions, answers, batch_size=5460):
    """Store questions and answers in the vector store in batches."""
    if not questions or not answers:
        print("No data to store.")
        return

    # Prepare documents
    documents = [
        {"page_content": question, "metadata": {"answer": answer}}
        for question, answer in zip(questions, answers)
    ]

    # Split into batches and store
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        texts = [doc["page_content"] for doc in batch]
        metadatas = [doc["metadata"] for doc in batch]

        # Store the batch in vector store
        Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas,
            persist_directory=vector_directory,
            collection_name="json_data"
        )
        print(f"Processed batch {i // batch_size + 1} of {(len(documents) - 1) // batch_size + 1}.")

    print("All questions and answers have been stored in the vector store.")


def check_db(query):
    """Query the vector store."""
    if not os.path.exists(vector_directory):
        print("Vector store not found. Please run the embedding process first.")
        return None

    vector_store = Chroma(
        persist_directory=vector_directory,
        embedding_function=embeddings,
        collection_name="json_data"
    )

    # Retrieve documents
    results = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 1},
    )
    response = results.invoke(query)

    if response:
        return response[0].metadata.get("answer", "No answer found.")
    return "No relevant results found."


def main():
    json_file_path = os.path.join(current_directory, "merged_answers.json")  # Replace with your JSON file path

    # Load questions and answers from JSON
    questions, answers = load_json_data(json_file_path)

    # Store them in the vector store
    store_in_vector_store(questions, answers)


if __name__ == "__main__":
    main()
    # Uncomment the following to test a query:
    print(check_db("What is Newton's first law?"))
