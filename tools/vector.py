import streamlit as st
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from llm import llm, embeddings
from langchain.prompts import PromptTemplate

VECTOR_SEARCH_TEMPLATE="""
You are a movie expert. You find movies from user's given plot.

Use the following context to summarise movies to provide recommendation to the user. 

CONTEXT:
------
{context}

RULES:
------
If no context is returned, do not attempt to answer the question.
If there are more than one movies, separate them into bullet points 
For each movie, include the title, genre, plot, year, runtime, released, budget.

Question: {question}
Answer: 

"""
prompt = PromptTemplate(
    template=VECTOR_SEARCH_TEMPLATE, input_variables=["context","question"]
)

neo4jvector = Neo4jVector.from_existing_index(
    embeddings,                              # (1)
    url=st.secrets["NEO4J_URI"],             # (2)
    username=st.secrets["NEO4J_USERNAME"],   # (3)
    password=st.secrets["NEO4J_PASSWORD"],   # (4)
    index_name="moviePlots",                 # (5)
    node_label="Movie",                      # (6)
    text_node_property="plot",               # (7)
    embedding_node_property="embedding",     # (8)
    retrieval_query="""
RETURN
    node.plot AS text,
    score,
    {
        title: node.title,
        directors: [ (person)-[:DIRECTED]->(node) | person.name ],
        actors: [ (person)-[r:ACTED_IN]->(node) | [person.name, r.role] ],
        tmdbId: node.tmdbId,
        source: 'https://www.themoviedb.org/movie/'+ node.tmdbId
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
