from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import json
import numpy as np
import faiss
from dotenv import load_dotenv

load_dotenv()

# Load documents from a JSON file
def load_documents_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    documents = [f"{item['title']} {item['description']} {' '.join(item['links'])}" for item in data]
    return documents

# Convert documents to embeddings and create a FAISS index
def create_faiss_index_from_docs(docs):
    embeddings_model = OpenAIEmbeddings()
    doc_embeddings = np.vstack([embeddings_model.embed_query(doc) for doc in docs])
    d = doc_embeddings.shape[1]  # Dimension of embeddings
    index = faiss.IndexFlatL2(d)  # Using L2 distance
    index.add(doc_embeddings)
    return index

# Main function to execute RAG with sources
def execute_rag_with_sources(file_path, user_input_question):
    llm = ChatOpenAI()
    docs = load_documents_from_json(file_path)  # Load documents
    faiss_index = create_faiss_index_from_docs(docs)  # Create FAISS index from documents
    
    # Embed the user query
    embeddings_model = OpenAIEmbeddings()
    query_embedding = embeddings_model.embed_query(user_input_question)
    query_embedding = np.array(query_embedding).reshape(1, -1)  # Reshape for FAISS
    
    # Find the most similar document(s)
    D, I = faiss_index.search(query_embedding, 1)  # Search for the most similar document; adjust as needed
    
    # Assuming you have a method to generate a response based on the most relevant document
    most_relevant_doc_index = I[0][0]
    most_relevant_doc = docs[most_relevant_doc_index]
    print(f"Most relevant document: {most_relevant_doc}")
    
    # Generate a response based on the most relevant document (simplified example)
    # Here, you'd use your LLM or another method to generate an answer based on the document
    answer = f"Based on the document: {most_relevant_doc}"
    return answer

# Example usage
if __name__ == "__main__":
    file_path = "url_data.json"  # Update this to your JSON file path
    user_input_question = "What is ActBlue"  # Your query
    answer = execute_rag_with_sources(file_path, user_input_question)
    print(answer)
