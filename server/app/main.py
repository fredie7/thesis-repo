from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.docstore.document import Document  # Correct import for Document class

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
print("API_KEY===>",openai_api_key)

if not openai_api_key:
    raise ValueError("Please provide the OPENAI_API_KEY")


# Define the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://cdd-app.vercel.app"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Define the request model
class ChatRequest(BaseModel):
    question: str

# Information retrieval from the CSV file using the specified columns
def extract_csv_info(file_path):
    df = pd.read_csv(file_path)
    
    # Concatenate relevant columns into a single text field for each row
    df['combined_text'] = (
        df['Patient Question'].fillna('') + ' ' +
        df['Distorted part'].fillna('') + ' ' +
        df['Dominant Distortion'].fillna('') + ' ' +
        df['Secondary Distortion (Optional)'].fillna('')
    )
    
    # Convert each row into a Document object
    documents = [Document(page_content=text) for text in df['combined_text'].tolist()]
    
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
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_messages([
    ("user", (
        "If the user greets you (e.g., 'Hi', 'Hello', 'Howdy'), respond warmly and playfully, e.g., 'I identify cognitive distortions - can you please share with me on how are you feeling today?'"
        "After the your first response that starts with 'I identify cognitive distortions', don't start with it again. Continue the folow of the conversation until you identify cognitive distortions"
        "If no greeting is detected, still start with a friendly, 'I identify cognitive distortions - Can you please share with me on how are you feeling?'"
        "If the user expresses gratitude (e.g., 'Thanks', 'Thank you'), reply with a cheerful 'You're welcome!'"
        "If the user's input has nothing to do with noticable cognitive distortions, gently steer them back with, 'Oops! I’m here to help with cognitive distortions. Please let’s avoid discussing outside that!'"
        "Engage in a conversational, natural, and light-hearted way while maintaining professionalism."
        
        "### Task:"
        "1. Identify if the user's message contains cognitive distortions."
        "2. If distortions are present, identify the **top 2** and explain them concisely."
        "3. If no distortions are detected, respond with, continue with the flow of the conversation but be in control of the questions that lead you to identifying cognitive distortion"

        "### Guidelines:"
        "- **Be personable and engaging**, as if chatting with a friend who also happens to be great at cognitive distortion detection!"
        "- **Avoid asterisks** in responses."
        "- Format responses so that each identified cognitive distortion appears on a **new line**, followed by a colon and a **one- or two-sentence explanation**."
        "- After identifying distortions, let the user know the cognitive distortions you identified **without giving direct advice**."
        "- If the user asks questions, respond **within the context of cognitive distortions and mental health.**"

        "### Common Cognitive Distortions to Detect:"
        "1. **Personalization:** Taking blame for things beyond your control. *'My friend didn’t text back—what did I do wrong?'*"
        "2. **Mind Reading:** Assuming you know what others think. *'They must think I’m stupid!'*"
        "3. **Overgeneralization:** Making broad conclusions from limited experiences. *'I failed once, so I’ll always fail.'*"
        "4. **All-or-Nothing Thinking:** Seeing things as black and white. *'If I don’t ace this test, I’m a failure.'*"
        "5. **Emotional Reasoning:** Assuming feelings = facts. *'I feel useless, so I must be.'*"
        "6. **Labeling:** Defining yourself/others with fixed labels. *'I’m just bad at everything.'*"
        "7. **Magnification:** Blowing problems out of proportion. *'I made a mistake, so I’m doomed.'*"
        "8. **Mental Filter:** Focusing only on negatives. *'I got one negative comment, so I must be awful.'*"
        "9. **Should Statements:** Placing rigid rules on yourself. *'I should never make mistakes.'*"
        "10. **Fortune-Telling:** Predicting the future negatively. *'I just know today will be awful.'*"

        "{context}"
    )),
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
        ("user", "Given the above conversation, generate a search query to get information relevant to the conversation.Answer the user's questions based on the context and make the answer short.Given the mental health situation of a user, our task is to: 1. Identify if there is cognitive thinking distortion in the user's text. 2. Please first answer: Is there cognitive distortion in the thinking of the user? On a whole line, Answer 'Well, I identify possible cognitive distortion' or 'No, I do not identify possible cognitive distortion', then from the next line go on to explain further starting with the cognition mode in bold.Let every response starting with the cognition mode start on a new line.Put each answer on separate lines and don't include '\n' nor '\n1'. 3. Then answer: Recognize the specific types of the cognitive distortion in the user's thought process. There may be one type of cognitive distortion or multiple types involved. If there are multiple types, please give the top 2 dominant ones.Here we consider the following top 10 common thinking distortions in the order of: Cognitive Distortion Type, Interpretation, Example Distorted thought.Cognitive Distortion Type, Interpretation, Example Distorted thought. 1. Personalization, Personalizing or taking up the blame for a situation that in reality involved many factors and was out of the person’s control, My son is pretty quiet today. I wonder what I did to upset him. 2. Mind Reading, Suspecting what others are thinking or what are the motivations behind their actions, My house was dirty when my friends came over, they must think I’m a slob! 3. Overgeneralization, Major conclusions are drawn based on limited information, Last time I was in the pool I almost drowned so I am a terrible swimmer and should not go into the water again. 4. All-or-nothing thinking, Looking at a situation as either black or white or thinking that there are only two possible outcomes to a situation, If I cannot get my Ph.D. then I am a total failure.5. Emotional reasoning, Letting one’s feeling about something overrule facts to the contrary, Even though Steve is here at work late every day I know I work harder than anyone else at my job.6. Labeling, Giving someone or something a label without finding out more about it/them, My daughter would never do anything I disapproved of.7. Magnification, Emphasizing the negative or playing down the positive of a situation, My professor said he made some corrections on my paper so I know I’ll probably fail the class. 8. Mental filter, Placing all one’s attention or seeing only the negatives of a situation, My husband says he wishes I was better at housekeeping so I must be a lousy wife. 9. Should statements, Should statements appear as a list of ironclad rules about how a person should behave as this could be about the speaker themselves or other. It is NOT necessary that the word 'should' or its synonyms (ought to, must etc.) be present in the statements containing this distortion, I should get all A’s to be a good student. 10. Fortune-telling, This distortion is about expecting things to happen a certain way or assuming that things will go badly. Counterintuitively, this distortion does not always have future tense, I was afraid of job interviews so I decided to start my own thing ")
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
csv_file_path = "annotated_data.csv"
documents = extract_csv_info(csv_file_path)
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