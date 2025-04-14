from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=1000, temperature=0)

store = {}

def get_chat_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", 
     """You are a fun and insightful Pokémon personality matcher.
You will ask the user 3 engaging personality or preference questions, one at a time.

Once the user has answered all 3, you will suggest a 1st generation Pokémon that fits their personality.
Be creative, but stay true to each Pokémon's known traits from the original Pokédex."""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="history"
)



session_id = "user_123"

print("Welcome to the Pokémon Personality Matchmaker!")
print("Answer 3 questions and discover your Gen 1 Pokémon match!\n")
print("Press Enter to Start")

# First automatic question from the bot
initial_response = chain_with_history.invoke(
    {"input": ""},
    config={"configurable": {"session_id": session_id}}
)
print("AI:", initial_response.content)

while True:
    user_input = input("you: ")
    if user_input.strip().lower() in ['exit', 'quit', 'bye']:
        print("AI Bot: Bye!")
        break

    response = chain_with_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    )

    print("AI:", response.content)

# ------- Example ---------
# response1 = chain_with_history.invoke(
#     {"input": "Hello! How are you?"},
#     config={"configurable": {"session_id": session_id}}
# )
# print("AI:", response1.content)

# response2 = chain_with_history.invoke(
#     {"input": "What was my previous message?"},
#     config={"configurable": {"session_id": session_id}}
# )
# print("AI:", response2.content)

print("\nConversation History:")
for message in store[session_id].messages:
    print(f"{message.type}: {message.content}")