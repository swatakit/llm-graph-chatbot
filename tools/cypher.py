from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

from llm import llm
from graph import graph

CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about claims and provide information.
Convert the user's question based on the schema.
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

If no context is returned, do not attempt to answer the question.

Use Neo4j 5 Cypher syntax.  When checking a property is not null, use `IS NOT NULL`.

Example Cypher Statements:

1. Find customer and contact information:
```
MATCH (p:Phone)-[:OWNS_PHONE]-(c:Customer)-[:OWNS_EMAIL]-(e:Email)
WHERE c.name='Devon Q. White'
RETURN c.name AS name, p.phoneNumber AS phoneNumer, e.email AS email
```

2. Find phone numbers shared by 2 or more customers
```
MATCH (p:Phone)<-[:OWNS_PHONE]-(c:Customer)
WITH p, count(c) AS numCustomers
WHERE numCustomers >= 2
MATCH (p)<-[:OWNS_PHONE]-(c:Customer)
RETURN p.phoneNumber, collect(c.name) AS CustomerNames
```

3. Find emails shared by 2 or more customers
```
MATCH (e:Email)<-[:OWNS_EMAIL]-(c:Customer)
WITH e, count(c) AS numCustomers
WHERE numCustomers >= 2
MATCH (e)<-[:OWNS_EMAIL]-(c:Customer)
RETURN e.email, collect(c.name) AS CustomerNames
```

4. Find the connections among customer, claim, agent, hospital, phone and email
```
MATCH (c:Customer)-[:FILED_CLAIM]->(clm:Claim)<-[:PROVIDED_MEDICAL_SERVICE]-(h:Hospital),
      (a:Agent)-[:SERVICED_CLAIM]->(clm),
      (c)-[:OWNS_PHONE]->(p:Phone),
      (c)-[:OWNS_EMAIL]->(e:Email)
RETURN c AS Customer, p AS Phone, e AS Email, clm AS Claim, h AS Hospital, a AS Agent
```

Schema:
{schema}

Question:
{question}
"""

cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)

cypher_qa = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True,
    cypher_prompt=cypher_prompt
)


