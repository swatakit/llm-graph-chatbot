from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

from llm import llm
from graph import graph

CYPHER_GENERATION_TEMPLATE = """
Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Question:
{question}

Cypher examples:

1. Find a customer and contact information
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
RETURN c.name AS Customer, p.phoneNumber AS Phone, e AS Email, clm.claimId AS Claim, h.name AS Hospital, a.name AS Agent
```

5. Find customers associated with an Agent
```
MATCH (c:Customer)-[:FILED_CLAIM]->(:Claim)<-[:SERVICED_CLAIM]-(a:Agent)
WHERE a.name='Avery H. Jackson'
RETURN c.name AS Customer
```

"""

cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)

cypher_qa_prompt = """The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.

Here is an example of a question and helpful answer:
Question: Which customers have an association with agent Avery H. Jackson?
Context:[Customer: Devon Q. Allen, Customer: Ellis L. Scott]
Helpful Answer: Devon Q. Allen, Ellis L. Scott has association with agent Avery H. Jackson.

Follow this example when generating answers.
If the provided information is empty, say that you don't know the answer.

Information:
{context}

Question: {question}
Helpful Answer:
"""

qa_prompt = PromptTemplate(input_variables=["context","question"], template=cypher_qa_prompt)

cypher_qa = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True,
    return_intermediate_steps=True,
    cypher_prompt=cypher_prompt,
    qa_prompt=qa_prompt
)


