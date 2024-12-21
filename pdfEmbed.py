import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import PyPDF2

# Initialize embeddings
embeddings = OllamaEmbeddings(model="all-minilm:33m")

# Set up directories
current_directory = os.path.dirname(os.path.abspath(__file__))
vector_directory = os.path.join(current_directory, "db", "chroma_db_physics_recursive")

def pdf_text_loader(file_path):
    # Check if the PDF file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    pdf_text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            pdf_text += page.extract_text()
    return pdf_text

def create_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = [Document(page_content=text)]
    return splitter.split_documents(documents)


def store_in_vector_store(docs):
    # Check if the docs list is not empty
    if not docs:
        print("No documents to store.")
        return

    # Store in vector store without printing docs
    Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=vector_directory,
        collection_name="physics"
    )
    print("Documents have been stored in the vector store.")

def check_db(query):
    # Check if the vector store exists
    if not os.path.exists(vector_directory):
        print("Vector store not found. Please run the embedding process first.")
        return
    
    vector_store = Chroma(
        persist_directory=vector_directory,
        embedding_function=embeddings,
        collection_name="physics"
    )
    
    # print("hello 1")
    # Retrieve documents and sco
    results = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k":1},
    )
    # print("hello 2")
    response = results.invoke(query)

    
    document = ""
    for doc in response:
        document += doc.page_content
        # print(doc.page_content)
    
    return document
    

def main():
    pdf_path = os.path.join(current_directory, "D:\\Codes\\cse299phychatbot\\physics_notes.pdf")
    
    # Load and process the PDF
    pdf_text = pdf_text_loader(pdf_path)
    
    # No need to print the full document content
    docs = create_chunks(pdf_text)
    
    # Store documents in the vector store
    store_in_vector_store(docs)
    # print("hello 3")
    # Example query to check the database
    # check_db(query="Ideal gas fundementals?")




if __name__ == "__main__":
    # Uncomment this line if you want to process and store the PDF
    main()
    
    # print(check_db("Newton's first law"))

