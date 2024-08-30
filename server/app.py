from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQA
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

import os
import re  # Import the regex module

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

from langchain_objectbox.vectorstores import ObjectBox
from langchain_openai import OpenAIEmbeddings

# Load documents from the web
loader = WebBaseLoader([
    "https://www.verywellmind.com/what-is-cognitive-behavior-therapy-2795747",
    "https://en.wikipedia.org/wiki/Coping",
    "https://www.ncbi.nlm.nih.gov/books/NBK279297/",
    "https://my.clevelandclinic.org/health/treatments/21208-cognitive-behavioral-therapy-cbt",
    "https://www.psychologytoday.com/intl/basics/cognitive-behavioral-therapy",
    "https://www.ncbi.nlm.nih.gov/books/NBK470241/",
    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8489050/"
])

web_content_list = loader.load()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(web_content_list)

# Initialize vector store
vector = ObjectBox.from_documents(documents, OpenAIEmbeddings(), embedding_dimensions=768)

# Set up retriever and document chain
retriever = vector.as_retriever()

prompt = ChatPromptTemplate.from_template("""
Answer the following question based on the provided context. Think step by step before providing a detailed answer.
<context>
{context}
</context>
Question: {input}
""")

llm = ChatOpenAI(model="gpt-4o", temperature=0)
document_chain = create_stuff_documents_chain(llm, prompt)

retrieval_chain = create_retrieval_chain(retriever, document_chain)

# Clean up the response to remove unwanted characters
def clean_response(response: str) -> str:
    # Remove multiple newlines and spaces
    cleaned = re.sub(r'\s+', ' ', response).strip()
    # Remove non-alphabetical characters (optional, depends on what you want to clean)
    cleaned = re.sub(r'[^a-zA-Z0-9,.!? ]', '', cleaned)
    return cleaned

# Define API endpoint
res = retrieval_chain.invoke({"input": "Explain mental health"})
cleaned_res = clean_response(res['answer'])  # Clean the response
print(cleaned_res)
