from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate

from llm import llm
from graph import graph

CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about movies and provide recommendations.
Convert the user's question based on the schema.
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

If no context is returned, do not attempt to answer the question.

Fine Tuning:

For movie titles that begin with "The", move "the" to the end. For example "The 39 Steps" becomes "39 Steps, The" or "the matrix" becomes "Matrix, The".

Use Neo4j 5 Cypher syntax.  When checking a property is not null, use `IS NOT NULL`.

Example Cypher Statements:

1. Find movies and their genres:
```
MATCH (m:Movie)-[:IN_GENRE]->(g)
WHERE m.title = "Goodfellas"
RETURN m.title AS title, collect(g.name) AS genres
```

2. Recommend a movie by actor:
```
MATCH (subject:Person)-[:ACTED_IN|DIRECTED]->(m)<-[:ACTED_IN|DIRECTED]-(p),
  (p)-[role:ACTED_IN|DIRECTED]->(m2)
WHERE subject.name = "Al Pacino"
RETURN
  m2.title AS recommendation,
  collect([ p.name, type(role) ]) AS peopleInCommon,
  [ (m)-[:IN_GENRE]->(g)<-[:IN_GENRE]-(m2) | g.name ] AS genresInCommon
ORDER BY size(incommon) DESC, size(genresInCommon) DESC LIMIT 2
```

3. How to find how many degrees of separation there are between two people:
```
MATCH path = shortestPath(
  (p1:Person {{name: "Actor 1"}})-[:ACTED_IN|DIRECTED*]-(p2:Person {{name: "Actor 2"}})
)
WITH path, p1, p2, relationships(path) AS rels
RETURN
  p1 {{ .name, .born, link:'https://www.themoviedb.org/person/'+ p1.tmdbId }} AS start,
  p2 {{ .name, .born, link:'https://www.themoviedb.org/person/'+ p2.tmdbId }} AS end,
  reduce(output = '', i in range(0, length(path)-1) |
    output + CASE
      WHEN i = 0 THEN
       startNode(rels[i]).name + CASE WHEN type(rels[i]) = 'ACTED_IN' THEN ' played '+ rels[i].role +' in 'ELSE ' directed ' END + endNode(rels[i]).title
       ELSE
         ' with '+ startNode(rels[i]).name + ', who '+ CASE WHEN type(rels[i]) = 'ACTED_IN' THEN 'played '+ rels[i].role +' in '
    ELSE 'directed '
      END + endNode(rels[i]).title
      END
  ) AS pathBetweenPeople
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


