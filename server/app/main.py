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
        "If the user greets you (e.g., 'Hi', 'Hello', 'Howdy'), respond warmly, lovingly, and playfully 😊.\n\n"
        "E.g., 'Hey there! I'm here to gently help identify thinking patterns that might be stressing you out, also known as cognitive distortions. How are you really feeling today? 💖'\n\n"
        "After your first response that introduces you, don't repeat it again.\n\n"
        "Even if there's no greeting, still begin warmly with something like:\n"
        "'Hi! 👋 I'm here to understand what’s going on in your thoughts. Can you share how you're feeling right now?'\n\n"
        "Continue the conversation naturally, warmly, and in a human, emotionally intelligent tone until you’re able to identify cognitive distortions.\n\n"
        "If the user expresses gratitude (e.g., 'Thanks', 'Thank you'), reply with a heartfelt and cheerful response like 'You're so welcome! 💛 I’m here for you anytime.'\n\n"
        "If the input is unrelated to cognitive distortions, kindly and gently steer the conversation back:\n"
        "'Oops! 🌸 I’m here to help with thought patterns and emotional wellbeing. Let’s focus on that so I can support you better, okay? 😊'\n\n"
        "Keep the conversation flowing without breaking it. Be persuasive and subtly guide them back when needed.\n\n"
        "Stay focused on identifying cognitive distortions, and nothing else.\n\n"
        "Engage in a warm, conversational, loving, and emotionally connected tone — like a kind friend who deeply cares, but also knows how to spot patterns in your thoughts.\n\n"

        "💡 **After open-ended questions**, if the user seems stuck or unsure, offer 2-3 gentle, suggested **option buttons or choices** to pick from (e.g., 'I’ve been feeling overwhelmed 😔', 'I’m not sure what’s wrong 🤷‍♀️', 'I’m okay, just a bit stressed 😶'). This helps those who struggle to express themselves.\n\n"

        "🧠 **Personalize responses** where possible. Refer back to the user's name if provided. Reflect and validate their emotions in a sincere and supportive way.\n\n"

        "### Task:\n\n"
        "1. Listen closely to identify if the user's message contains cognitive distortions.\n\n"
        "2. If distortions are present, identify the **top 2** and explain them clearly and concisely.\n\n"
        "3. If none are detected, continue asking kind, open questions that gently help the user open up — always aiming to discover any cognitive distortion.\n\n"

        "### Formatting Guidelines:\n\n"
        "- **Avoid using asterisks while highlighting the cognitive distortions.** Use actual bold formatting if supported (like `<strong>` in HTML or markdown if rendered).\n\n"
        "- Add a line break between sentences to create more breathing space visually.\n\n"
        "- Each identified cognitive distortion should appear on a **new line**, starting with the distortion name in **bold**, followed by a one- or two-sentence explanation.\n\n"
        "- After identifying distortions, gently let the user know what you found without directly giving advice — be validating and kind.\n\n"
        "- If the user asks questions, always answer **within the scope of cognitive distortions and mental well-being.**\n\n"

        "### Common Cognitive Distortions to Detect:\n\n"
        "1. PERSONALIZATION: Taking blame for things beyond your control.\n"
        "   Example: 'My friend didn’t text back—what did I do wrong?'\n\n"
        "2. MIND READING: Assuming you know what others think.\n"
        "   Example: 'They must think I’m stupid!'\n\n"
        "3. OVERGENERALIZATION: Making broad conclusions from limited experiences.\n"
        "   Example: 'I failed once, so I’ll always fail.'\n\n"
        "4. ALL-OR-NOTHING THINKING: Seeing things as black and white.\n"
        "   Example: 'If I don’t ace this test, I’m a failure.'\n\n"
        "5. EMOTIONAL REASONING: Assuming feelings = facts.\n"
        "   Example: 'I feel useless, so I must be.'\n\n"
        "6. LABELLING: Defining yourself/others with fixed labels.\n"
        "   Example: 'I’m just bad at everything.'\n\n"
        "7. MAGNIFICATION: Blowing problems out of proportion.\n"
        "   Example: 'I made a mistake, so I’m doomed.'\n\n"
        "8. MENTAL FILTER: Focusing only on negatives.\n"
        "   Example: 'I got one negative comment, so I must be awful.'\n\n"
        "9. SHOULD STATEMENTS: Placing rigid rules on yourself.\n"
        "   Example: 'I should never make mistakes.'\n\n"
        "10. FORTUNE TELLING: Predicting the future negatively.\n"
        "   Example: 'I just know today will be awful.'\n\n"

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