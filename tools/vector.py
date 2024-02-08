import streamlit as st
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from llm import llm, embeddings
from langchain.prompts import PromptTemplate

VECTOR_SEARCH_TEMPLATE="""
You are a claim handler expert. You find claim information based provided narration.

Use the following context to summarise claim information to the user. 

CONTEXT:
------
{context}

RULES:
------
If no context is returned, do not attempt to answer the question.
If there are more than one claims, put them in a markdown table 

Question: {question}
Answer: 

"""
prompt = PromptTemplate(
    template=VECTOR_SEARCH_TEMPLATE, input_variables=["context","question"]
)

neo4jvector = Neo4jVector.from_existing_index(
    embeddings,                              
    url=st.secrets["NEO4J_URI"],             
    username=st.secrets["NEO4J_USERNAME"],   
    password=st.secrets["NEO4J_PASSWORD"],   
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
        hospitak: [ (hospital)-[:PROVIDED_MEDICAL_SERVICE]->(node) | hospital.name ]
    } AS metadata
"""
)

retriever = neo4jvector.as_retriever()

from langchain.chains import RetrievalQA

# kg_qa = RetrievalQA.from_chain_type(
#     llm,                  # (1)
#     chain_type="stuff",   # (2)
#     retriever=retriever,  # (3)
# )

# kg_qa = RetrievalQA.from_llm(
#     llm=llm,
#     retriever=retriever, 
#     verbose=True, 
#     return_source_documents=True
# )

kg_qa = RetrievalQA.from_chain_type(
    llm,                  # (1)
    chain_type="stuff",   # (2)
    retriever=retriever,  # (3)
    verbose=True,
    chain_type_kwargs={"prompt": prompt, 'verbose': True}
)
