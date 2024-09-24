from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import LLMChain
from langchain.schema.runnable import RunnableMap
from langchain.chains import RetrievalQA  
from langchain_pinecone import PineconeVectorStore
import json

from typing import Any, Dict, List
# Load environment variables from .env file
load_dotenv()

# This is the prompt used
template = """

You are a information retrieval AI. Format the retrieved information as a table or text


Use only the context for your answers, do not make up information

query: {query}

{context} 
"""

# Converts the prompt into a prompt template
prompt = ChatPromptTemplate.from_template(template)

# Initialize the ChatOpenAI model
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
docsearch = PineconeVectorStore(index_name="pdf", embedding=embeddings)
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    #return_source_documents=True,
    retriever=docsearch.as_retriever() #search_kwargs={"k": 5}
)
   

query="ammar education"
result = qa.invoke(query)
print(result)


# Send each query to the LLM twice, first with relevant knowledge from Pincone 
# and then without any additional knowledge.
def run_llm(query: str):
    result = qa.invoke(query)
    return result.get("result")