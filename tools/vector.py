import streamlit as st
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from llm import llm, embeddings
from langchain.prompts import PromptTemplate
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

VECTOR_SEARCH_TEMPLATE="""
You are a claim handler expert. You find claim information based provided narration or description.

Use the following context to summarise claim information to the user. 

CONTEXT:
------
{context}

RULES:
------
If no context is returned, do not attempt to answer the question.
If there are more than one claims, summarize key information in bullet points then compile the information into table format.

Question: {question}
Answer: 

"""
prompt = PromptTemplate(
    template=VECTOR_SEARCH_TEMPLATE, input_variables=["context","question"]
)

neo4jvector = Neo4jVector.from_existing_index(
    embeddings,                              
    url=NEO4J_URI,             
    username=NEO4J_USERNAME,   
    password=NEO4J_PASSWORD,   
    index_name="claimNarration",                 
    node_label="Claim",                      
    text_node_property="narration",               
    embedding_node_property="embedding",     
    retrieval_query="""
RETURN
    node.narration AS text,
    score,
    {
        claimId: node.claimId,
        disease: node.disease,
        customer: [ (customer)-[:FILED_CLAIM]->(node) | customer.name ],
        risk: node.risk,
        fraud: node.fraud,
        agent: [ (agent)-[:SERVICED_CLAIM]->(node) | agent.name ],
        hospital: [ (hospital)-[:PROVIDED_MEDICAL_SERVICE]->(node) | hospital.name ]
    } AS metadata
"""
)

retriever = neo4jvector.as_retriever()

from langchain.chains import RetrievalQA


kg_qa = RetrievalQA.from_chain_type(
    llm,                  
    chain_type="stuff",   
    retriever=retriever,  
    verbose=True,
    chain_type_kwargs={"prompt": prompt}
)
