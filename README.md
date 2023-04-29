# LangChainQA_Frontend_Integration

This project is a demonstration of the capabilities of using the LangChain framework. A question-answering bot was developed to answer relevant questions about products from JCrew's website. 

Key Technologies used:
- BeautifulSoup -> For webscraping JCrew's website
- OpenAI -> Underlying LLM to power the chatbot
- Chroma -> Vectorstore used for storing embeddings from text
- Vite.js -> Front-end
- Flask -> Hosting backend python server

### Refer to individual files for code-working and explanations.

## Instructions for running application
- Clone repo and run pip install -r requirements.txt within the backend folder to install relevant libraries
- Open two terminals, one for frontend, one for backend
  - Frontend: cd frontend; npm run dev
  - Backend: cd backend; python3 database_connection.py
- Navigate to http://localhost:5173/ and start the conversation with the chatbot

Illustration:
<img width="1440" alt="image" src="https://user-images.githubusercontent.com/29282668/235316099-cba1f6ee-be3f-419a-8a4b-1fb2d03959c1.png">

Work in progress:
Integrating the chatbot into a live website as a pop-up instead of taking up a whole webpage on its own.
