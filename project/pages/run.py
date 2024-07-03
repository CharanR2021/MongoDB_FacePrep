from pymongo import MongoClient
import streamlit as st
from langchain.llms import CTransformers
from langchain.agents import initialize_agent, Tool
from langchain_core.output_parsers import StrOutputParser
from langchain import LLMChain
from datetime import datetime

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['orders_db']  # Database name
dbc = db['orders']  # Collection name

# LangChain setup
llm = CTransformers(model='C:\\Users\\sucin\\Desktop\\MongoDB-Faceprep\\project\\llm\\mistral', 
                    model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",   
                    model_type='mistral',
                    temperature=0.8,
                    gpu_layers=0,
                    max_new_tokens=6000,
                    context_length=6000)

db_chain = LLMChain.from_llm(llm=llm, database=dbc, verbose=True)

# Tools setup for LangChain agent
tools = [
    Tool(
        name="Order_Database",
        func=db_chain.run,
        description="Useful for answering questions about products."
    )
]

# Initialize LangChain agent
agent = initialize_agent(tools=tools, llm=llm, agent_type="zero-shot-react-description", verbose=True)

# Streamlit UI
st.title('Order Tracking')
st.write("Enter your order ID and a question regarding your order, and I will help you track it.")

question = st.text_input("Enter your question:")

def is_valid_order_id(order_id):
    return order_id.isdigit() and len(order_id) == 6

if st.button("Submit"):
        full_question = f"Question: {question}"
        try:
            s="0"
            for i in question.split(" "):
                res = ''.join(filter(lambda i: i.isdigit(), i))
                if len(res)==6:
                     s=res        
            if len(s)==6:
                 
                output = agent.invoke(full_question, handle_parsing_errors=True)
                st.write(f"Answer: {output['output']}")
            else:
                st.write("Please provide your order id.")
                 
            
        except Exception as e:
            st.write(f"An error occurred: {e}")
