# Build a Health Claim ChatBot with OpenAI and Neo4j

## Description

This is a repository for a Cliam Chatbot backed by neo4j graph database.

If you are new to `OpenAI`, `LangChain`, and `Neo4j`, please explore the learning resources here.

|OpenAI| LangChain | Neo4j |
|------|-----------|-------|
| [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)| [LangChain for LLM Application Development](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/) | [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/) |
|[Building Systems with the ChatGPT API](https://www.deeplearning.ai/short-courses/building-systems-with-chatgpt/)| [LangChain: Chat with Your Data](https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data/) | [Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals/) |
|| [Functions, Tools and Agents with LangChain ](https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/)| [Graph Data Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals/) |
|| | [Importing CSV data into Neo4j](https://graphacademy.neo4j.com/courses/importing-cypher/) |


## Agent Tools List

- **General Chat**
  - *Description*: For general chat about disease, illness and symptom
  - *Function*: `llm.invoke`
  - *Discription*: This is the base LLM, Please note, the LLM is instructed to only respond to queries related to disease, illness and symptom.


- **Vector Search Index**
  - *Description*: Provides claims information based on narration using Vector Search
  - *Function*: `run_retriever`
  - *Discription*: ...


- **Graph Cypher QA Chain**
  - *Description*: Provides information about relationships among Customer, Claim, Agent, Hospital, Phone and Email.
  - *Function*: `run_cypher`
  - *Discription*: ..

## Installation

To run the application, you must install the libraries listed in `requirements.txt`.
```bash
pip install -r requirements.txt
```
## Running the application

Then run the `streamlit run` command to start the app on [http://localhost:8501/](http://localhost:8501/)

```bash
streamlit run app.py
```

## Download Neo4j Desktop 
Follow instruction on [neo4j daownload](https://neo4j.com/download/)

## Claim data
![Claim Data](img/claim-sample.png)

## Graph Database Schema

```Cypher
call db.schema.visualization()
```
![Data Model](img/schema-visualization.png)


