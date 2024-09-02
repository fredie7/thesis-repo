from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.history_aware_retriever import create_history_aware_retriever

# Define the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://my-frontend-domain.com"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# Define the request model
class ChatRequest(BaseModel):
    question: str

# Information retrieval from the web
def extract_web_info(urls):
    documents = []
    for url in urls:
        loader = WebBaseLoader(url)
        documents.extend(loader.load())
    
    split_docs = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20
    )
    splitDocs = split_docs.split_documents(documents)
    return splitDocs

# Create the vector store from documents
def create_vector_store(documents):
    embedding = OpenAIEmbeddings()
    vectorStore = FAISS.from_documents(documents, embedding=embedding)
    return vectorStore

# Create the chain for processing user queries
def create_recurring_chain(vectorStore):
    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the context and make the answer short: {context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])

    chain = create_stuff_documents_chain(
        llm=model,
        prompt=prompt
    )

    retriever = vectorStore.as_retriever(search_kwargs={"k": 3})

    retriever_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to get information relevant to the conversation.Make the answer short")
    ])
    history_aware_retriever = create_history_aware_retriever(
        llm=model,
        retriever=retriever,
        prompt=retriever_prompt
    )

    retrieval_chain = create_retrieval_chain(
        history_aware_retriever,
        chain
    )

    return retrieval_chain

# Initialize the documents and chain globally
urls = [
    "https://www.verywellmind.com/what-is-cognitive-behavior-therapy-2795747",
    "https://en.wikipedia.org/wiki/Coping",
    "https://www.ncbi.nlm.nih.gov/books/NBK279297/",
    "https://my.clevelandclinic.org/health/treatments/21208-cognitive-behavioral-therapy-cbt",
    "https://www.psychologytoday.com/intl/basics/cognitive-behavioral-therapy",
    "https://www.ncbi.nlm.nih.gov/books/NBK470241/",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8489050/"
]

documents = extract_web_info(urls)
vectorStore = create_vector_store(documents)
chain = create_recurring_chain(vectorStore)

# Initialize chat history
chat_history = []

@app.post("/ask")
async def chat(request: ChatRequest):
    global chat_history
    question = request.question
    
    # Process the chat and return the response
    try:
        response = chain.invoke({
            "chat_history": chat_history,
            "input": question,
        })
        answer = response["answer"]
        
        # Update chat history
        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=answer))
        
        return {"response": answer}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)