from flask import Flask, request
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from pdfEmbed import check_db  # Assuming this function retrieves relevant context from a vector store
from chat_history import ChatHistory  # Import the ChatHistory class

app = Flask(__name__)

# Initialize the model and chat history
MODEL = "gemma2:2b"
llm = Ollama(model=MODEL)
chat_history = ChatHistory()  # Create an instance of ChatHistory

# Define a prompt template that includes chat history for follow-up questions
template = """
    You are a physics expert. Answer questions based on the provided context first.
    If the context does not contain enough information, or if context is missing, answer the question using your general knowledge of physics.
    
    If the question contains terms like "it," "this," "that," or "tell me more," refer to the recent chat history to understand the user's intent.
    Also, if the question is a follow-up, provide additional information based on the recent chat history.
    Before saying you cannot answer, first check if the question refers to any previous history.

    Recent History (if relevant): {recent_history}

    Context: {context}
    Question: {question}

    If the question does not relate to any physics topics, respond with:
    "Sorry, I can only answer questions based on physics topics."
"""

prompt_template = PromptTemplate.from_template(template)

def get_response(question):
    # Keywords related to physics to check if question is about physics
    physics_keywords = ["physics", "motion", "force", "energy", "light", "wave", "electricity", 
                        "magnetism", "quantum", "relativity", "speed", "mass", "acceleration"]
    
    # Recognize specific physics constants and terms for special handling
    specific_terms = ["speed of light", "gravitational constant", "planck's constant", "boltzmann constant"]
    is_physics_question = any(keyword in question.lower() for keyword in physics_keywords) or any(term in question.lower() for term in specific_terms)

    # Extensive list of follow-up terms provided
    follow_up_terms = [
        "it", "this", "that", "tell me more", "more about", "first one", "second one", "explain more", "elaborate more", 
        "clarify more", "expand more", "details", "previous", "earlier", "before", "last one", "next one", "last thing", 
        "next thing", "last part", "next part", "last topic", "next topic", "example", "example of", "instance", 
        "instance of", "case", "case of", "situation", "situation of", "scenario", "scenario of", "circumstance", 
        "circumstance of", "condition", "condition of", "context", "context of", "background", "background of", 
        "preceding", "preceding one", "succeeding", "succeeding one", "subsequent", "subsequent one", "mathematical example", 
        "mathematical instance", "mathematical case", "mathematical situation", "mathematical scenario", "mathematical circumstance", 
        "mathematical condition", "mathematical context", "mathematical background", "mathematical preceding", 
        "mathematical succeeding", "mathematical subsequent", "mathematical illustration", "mathematical representation", 
        "mathematical model", "mathematical demonstration", "mathematical explanation", "mathematical proof", 
        "mathematical theorem", "mathematical formula", "mathematical equation", "mathematical concept", 
        "mathematical theory", "mathematical principle", "mathematical law", "mathematical rule", "mathematical concept", 
        "mathematical idea", "mathematical notion", "mathematical term", "mathematical definition", "mathematical property", 
        "mathematical characteristic", "mathematical feature", "mathematical aspect", "mathematical element", 
        "mathematical component", "mathematical part", "mathematical section", "mathematical segment", "mathematical portion", 
        "mathematical division", "mathematical fraction", "mathematical piece", "mathematical bit", "mathematical particle", 
        "mathematical unit", "mathematical module", "mathematical block", "mathematical object", "mathematical entity", 
        "mathematical thing", "mathematical stuff", "mathematical matter", "mathematical subject"
    ]
    is_follow_up = any(term in question.lower() for term in follow_up_terms)

    # Prepare recent history if it’s a follow-up question
    recent_history = ""
    context = ""
    if is_follow_up:
        # Retrieve the last two exchanges from chat history if available
        recent_history_entries = chat_history.get_history()[-2:]
        recent_history = "\n".join(
            [f"Q: {entry['question']}\nA: {entry['answer']}" for entry in recent_history_entries]
        )
    else:
        # Call check_db for non-follow-up questions
        context = check_db(question)
        if not context and not is_physics_question:
            # If it's not a physics question and context is empty, return disclaimer
            return "Sorry, I can only answer questions based on physics topics."
        elif not context and is_physics_question:
            # If it's a specific term or physics question but context is empty, use model knowledge
            context = "Use your general physics knowledge to answer."

    # Format the prompt with recent history (if any), context, and the question
    formatted_prompt = prompt_template.format(
        recent_history=recent_history,
        context=context,
        question=question
    )

    # Debug statements to check prompt content
    # print("DEBUG: Formatted prompt:")
    # print(formatted_prompt)

    # Get response from the LLM
    response = llm.invoke(formatted_prompt)
    
    # Store the question and response in chat history
    chat_history.add_entry(question, response)
    
    return response


@app.route("/ask", methods=["POST"])
def ask():
    """Handles general queries using chat history for follow-up questions."""
    json_content = request.json
    question = json_content.get("query")
    
    answer = get_response(question)
    return {"answer": answer}

@app.route("/clear_history", methods=["POST"])
def clear_history():
    """Endpoint to clear the chat history."""
    chat_history.clear_history()
    return {"status": "Chat history cleared"}

def delete_chat_history():
    chat_history.clear_history()
    print("Chat history deleted.")

# Only run the interactive loop if this file is executed directly
if __name__ == "__main__":
    print("Welcome to Physics Chatbot!")

    while True:
        text = input("Ki jante chas? : ")  
        if text in ["exit", "quit"]:
            print("Hedar pola tumi!")  
            break
        elif text == "delete history":
            delete_chat_history()
            continue

        answer = get_response(text)
        print(answer)

    # Display chat history at the end of the session
    history = chat_history.get_history()
    if not history:
        print("No chat history available.")
    else:
        for idx, entry in enumerate(history, 1):
            print(f"Chat {idx}:")
            print(f"  Question: {entry['question']}")
            print(f"  Answer: {entry['answer']}\n")
