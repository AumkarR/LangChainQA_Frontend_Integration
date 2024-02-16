from dotenv import load_dotenv #Loading .env file containing private OpenAI's API Key
from langchain_community.document_loaders import DirectoryLoader #Importing DirectoryLoader which allows importing all contents withint a folder into a database
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma #Importing Chroma, a vectorstore that is able to chunk similar data together; Any other vectorstores found on https://python.langchain.com/en/latest/modules/indexes/vectorstores.html?highlight=vectorstores
from langchain.chains import RetrievalQA #Importing the RetrievalQA module from Langchain to initiate a retrieval question/answering mechanism
from langchain_openai import OpenAI #I will be using an OpenAI model for the LLM of choice since I am most familiar with it, but any LLM can be used from this list: https://python.langchain.com/en/latest/modules/models/llms/integrations.html
from langchain_openai import OpenAIEmbeddings #Importing the embedding library to ensure that the ChromaDB is able to cluster similar data
import chromadb #Importing ChromaDB to access the settings option to store the database into a local folder


load_dotenv() #Loading the .env file into the working document

loader = DirectoryLoader('product_information', glob="**/*.html") #Product Information contains the HTML files generated from the scraping.py file

documents = loader.load() #The load function is used to generate a documents variable

text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0) #Importing a text splitter to create chunks of text that can be stored into a database through embeddings
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(texts, embeddings, persist_directory="db_files") #Storing all of the split texts into the Chroma database, which are grouped according to their embeddings into db_files

qa = RetrievalQA.from_chain_type ( #Using the RetrievalQA module to choose the LLM, chain_type and retriever of choice
    llm = OpenAI(),
    chain_type = "stuff", #Stuff was used as the chain_type here, but any chain type from https://python.langchain.com/en/latest/modules/chains/index_examples/qa_with_sources.html#the-stuff-chain can be used as per the requirements
    retriever = vectorstore.as_retriever() #The Chroma vectorstore that we generated is retrieved for question/answering
)

def query(q): #A query function is defined to take user's input query and return the answer based on the question/answering logic contained above
    return qa.run(q)

# print(query("tell me about Technicolor floral top"))