import os
import fitz
from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
import warnings
from langchain.text_splitter import CharacterTextSplitter

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
current_directory = os.path.dirname(os.path.abspath(__file__))
vector_directory = os.path.join(current_directory, "db", "chroma_db_physics")

# Ensure the vector directory exists
os.makedirs(vector_directory, exist_ok=True)

def check_db():
    # Load the persisted Chroma database
    client = Chroma(
        collection_name="physics",
        persist_directory=vector_directory,
        embedding_function=embedding_model
    )      

    # Retrieve relevant documents based on a query
    retriever = client.as_retriever(search_type="similarity")
    all_docs = retriever.get_relevant_documents("Newton's first law")  # Use appropriate method
    
    # Optionally, print the retrieved documents
    for doc in all_docs:
        print(f"Document content: {doc.page_content}\n")


warnings.filterwarnings("ignore", category=FutureWarning)

def get_text_from_pdf(pdf_path: str):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def split_text(text, chunk_size=1000, overlap=100):
    # Use the text splitter to create documents with overlapping chunks
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.create_documents(text)

def embedd(page_text):
    # Split the text into chunks
    docs = split_text(page_text)
    print("Chunking done.")
    
    # Embed the chunks and store in the Chroma database
    vector = Chroma.from_documents(
        collection_name="physics", 
        documents=docs, 
        embedding=embedding_model, 
        persist_directory=vector_directory
    )
    vector.persist()  # Persist the embeddings in the directory

if __name__ == "__main__":
    # Load text from PDF and embed into vector store
    pdf_path = "D:/Codes/cse299phychatbot/physics_notes.pdf"
    page_text = get_text_from_pdf(pdf_path)
    embedd(page_text)
    
    # Check the vector database by querying it
    check_db()
