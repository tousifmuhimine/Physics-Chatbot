from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pdfEmbed import check_db  # Assuming this queries the vector store for relevant context
from chat_history import ChatHistory  # For managing chat history

# Set up API key and Gemini LLM
API_KEY = "AIzaSyC2Dntwz2v0xnQZ3FU19enh9ocLvs31UQw"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=API_KEY)

# Create an instance of ChatHistory
chat_history = ChatHistory()

# Define the prompt template
template = """
    You are a physics expert. 

    Use the context below to answer the question.

    Context: {context}

    Question: {question}"""

# Initialize the PromptTemplate from the template
prompt = PromptTemplate.from_template(template)

# Function to get the response using the Gemini model and the context retrieved from check_db
def get_response(question):
    # Retrieve context from the vector store using check_db
    context = check_db(question)  # Assuming check_db returns the relevant documents
    if not context:
        return "Sorry, I can only answer questions related to physics."

    # Format the prompt with the retrieved context and the user question
    formatted_prompt = prompt.format(context=context, question=question)
    
    # Get response from the LLM (Gemini)
    response = llm.invoke(formatted_prompt)
    
    # Store the question and response in chat history
    chat_history.add_entry(question, response.content if hasattr(response, 'content') else response)
    
    # Return the response content
    return response.content if hasattr(response, 'content') else response

# Function to delete chat history
def delete_chat_history():
    chat_history.clear_history()
    print("Chat history deleted.")

# Main loop to interact with the chatbot
if __name__ == "__main__":
    print("Welcome to Physics Chatbot!")

    while True:
        text = input("Ki jante chas? : ")  # User input for the question
        if text in ["exit", "quit"]:
            print("Hedar pola tumi!")  # Fun exit message
            break
        elif text == "delete history":
            delete_chat_history()
            continue

        # Get the answer for the question and print the response
        answer = get_response(text)
        print(answer)

    # Optionally, retrieve and display chat history
    history = chat_history.get_history()
    if not history:
        print("No chat history available.")
    else:
        for idx, entry in enumerate(history, 1):
            print(f"Chat {idx}:")
            print(f"  Question: {entry['question']}")
            print(f"  Answer: {entry['answer']}\n")
