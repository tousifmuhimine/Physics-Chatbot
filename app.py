import streamlit as st
import time
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from jsonEmbed import check_db as check_json_db  # Import the JSON database query function
from pdfEmbed import check_db as check_pdf_db  # Import the PDF database query function
from chat_history import ChatHistory  # Import the ChatHistory class

# Initialize the model and chat history
MODEL = "gemma2:2b"
llm = Ollama(model=MODEL)
chat_history = ChatHistory()  # Create an instance of ChatHistory

# Define a prompt template that includes chat history for follow-up questions
template = """
You are a physics expert. Your job is to answer questions based on the provided context first. If the question is ambiguous (e.g., contains terms like "he," "his," "this," or "that"), refer to the recent history to clarify the subject.

If the question is a follow-up (e.g., asking "what else" or "tell me more"), provide additional details based on the recent history. Use the recent subject explicitly when needed.

Recent History (if relevant):
Q: {recent_history}

Context:
{context}

Question:
{question}

Guidelines:
- If the question is about physics but lacks context, use your general knowledge of physics to answer.
- If the question is not related to physics, respond with: "Sorry, I can only answer questions based on physics topics."
- Ensure your response aligns with the current question and the recent history.

Answer:
"""


prompt_template = PromptTemplate.from_template(template)

# Streamlit setup
st.set_page_config(page_title="Physics Master", page_icon="💬")
st.title("💬 Physics Master 👨🏼‍🎓")

# Display model in sidebar
st.sidebar.write("**Model:**", MODEL)

# Initialize chat history and response time in session state if not already done
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "last_response_time" not in st.session_state:
    st.session_state["last_response_time"] = 0.0

# Function to clear chat history
def clear_chat_history():
    st.session_state["messages"] = []
    chat_history.clear_history()  # Also clear the persistent chat history

# Button to clear chat history
if st.sidebar.button("Clear Chat History"):
    clear_chat_history()


def get_response(question):

     # Physics-related keywords
    physics_keywords = [
        "physics", "motion", "force", "energy", "light", "wave", "electricity", "magnetism",
        "quantum", "relativity", "speed", "mass", "acceleration", "vector", "gravity",
        "thermodynamics", "entropy", "momentum", "inertia", "friction", "velocity",
        "work", "power", "pressure", "density", "frequency", "amplitude", "oscillation",
        "resistance", "current", "voltage", "capacitance", "inductance", "circuit",
        "particle", "atom", "molecule", "nucleus", "electron", "proton", "neutron",
        "photon", "boson", "fermion", "neutrino", "gluon", "quark", "higgs",
        "field", "radiation", "electromagnetic", "optics", "reflection", "refraction",
        "diffraction", "interference", "polarization", "lens", "mirror", "prism",
        "black hole", "cosmology", "universe", "galaxy", "solar system",
        "planet", "star", "neutron star", "white dwarf", "supernova", "big bang",
        "dark matter", "dark energy", "space-time", "relativity", "Einstein", "Newton",
        "Maxwell", "Planck", "Bohr", "Heisenberg", "Schrodinger", "uncertainty",
        "laser", "atomic", "nuclear", "fission", "fusion", "thermal", "insulator",
        "fluid", "viscosity", "buoyancy", "turbulence", "plasma", "mechanics", "kinematics",
        "dynamics", "elasticity", "tension", "compression", "shear", "ideal gas",
        "gas law", "PV=nRT", "optical", "lens", "focal point", "ICM", "moment of inertia",
    ]

    # Specific terms for handling
    specific_terms = [
        "speed of light", "gravitational constant", "planck's constant", "boltzmann constant",
        "universal gas constant", "speed of sound", "acceleration due to gravity", "elementary charge",
        "mass of electron", "types of energy"
    ]
    is_physics_question = any(keyword in question.lower() for keyword in physics_keywords) or any(term in question.lower() for term in specific_terms)


    # Follow-up detection
    follow_up_terms = [
        "it", "this", "that", "he", "she", "tell me more", "more about", "first one", "second one",
        "explain more", "expand more", "details", "third person", "previous", "earlier", "before",
        "last one", "next one", "last thing", "next thing", "last part", "next part",
        "last topic", "next topic", "example", "instance", "case", "situation", "scenario",
        "condition", "background", "preceding", "succeeding", "subsequent", "formula",
        "concept", "principle", "law", "definition", "property", "characteristic",
        "aspect", "element", "component", "unit", "object", "term", "explanation",
        "proof", "theorem", "equation", "idea", "theory", "notion", "illustration",
        "representation", "yes", "okay", "go on", "continue", "mathematical example", "example", "what else","what is","what are"
        "explain", "elaborate", "clarify", "specify", "detail", "describe", "demonstrate","exxplain more","above problem","above question","above topic","above concept","above theory","above equation","above formula","above principle","above law","above definition","above property","above characteristic","above aspect","above element","above component","above unit","above object","above term","above explanation","above proof","above theorem","above idea","above theory","above notion","above illustration","above representation","above yes","above okay","above go on","above continue","above mathematical example","above example"
    ]
    is_follow_up = any(term in question.lower() for term in follow_up_terms)

    # Step 1: Check if the question is a follow-up and fetch history
    recent_history = ""
    history = chat_history.get_history()  # Get full history of chat

    if history:  # If there's any history at all
        recent_history = "\n".join([f"Q: {entry['question']}\nA: {entry['answer']}" for entry in history])

    # Retrieve context only if not a follow-up
    context = check_json_db(question) if not is_follow_up else ""
    if not context:
        context = check_pdf_db(question)

    # Fallback to general physics knowledge
    if not context and is_physics_question:
        context = '''Answer based on your general knowledge of physics only.
                    For outside physics questions, respond with: 'Sorry, I can only answer questions based on physics topics.'
                    If you find any topic related to biology or chemistry, please do not respond with answers; instead, say you cannot answer that. For example, "What is genetics?" is a biology question.
                    '''
    # Format the prompt with recent history, context, and current question
    formatted_prompt = prompt_template.format(
        recent_history=recent_history,
        context=context,
        question=question
    )

    # Generate response and calculate processing time
    start_time = time.time()
    response = llm.invoke(formatted_prompt)
    processing_time = time.time() - start_time

    # Add the question and response to chat history
    chat_history.add_entry(question, response)

    return response, processing_time



# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Check for new user input
if prompt := st.chat_input("Ask a question about physics!"):
    # Append user input to chat history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display the assistant's response
    response, processing_time = get_response(prompt)
    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.session_state["last_response_time"] = processing_time

    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)

# Update sidebar with the most recent response time
if st.session_state["last_response_time"]:
    st.sidebar.write(f"Response time: {st.session_state['last_response_time']:.2f} seconds")
