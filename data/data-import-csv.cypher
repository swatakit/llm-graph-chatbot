// CREATE Customer
CREATE CONSTRAINT Customer_name IF NOT EXISTS 
FOR (x:Customer) REQUIRE x.name IS UNIQUE;
LOAD CSV WITH HEADERS FROM 'file:///customers.csv' AS row
MERGE (c:Customer {name: row.Customer})
SET 
	c.name = row.Customer,
	c.gender = row.Gender;
	
	
// CREATE Phone
CREATE CONSTRAINT Phone_phoneNumber IF NOT EXISTS 
FOR (x:Phone) REQUIRE x.phoneNumber IS UNIQUE;
LOAD CSV WITH HEADERS FROM 'file:///phones.csv' AS row
MERGE (p:Phone {phoneNumber: row.PhoneNumber})
SET 
	p.phoneNumber = row.PhoneNumber;

// Create relationship Customer OWNS Phone
LOAD CSV WITH HEADERS
FROM 'file:///owns_phone.csv'  AS row
MATCH (c:Customer {name: row.Customer})
MATCH (p:Phone {phoneNumber: row.PhoneNumber})
MERGE (c)-[r:OWNS_PHONE]->(p);


// CREATE Email
CREATE CONSTRAINT Email_email IF NOT EXISTS 
FOR (x:Email) REQUIRE x.email IS UNIQUE;
LOAD CSV WITH HEADERS FROM 'file:///emails.csv' AS row
MERGE (p:Email {email: row.Email})
SET 
	p.email = row.Email;

// Create relationship Customer OWNS Email
LOAD CSV WITH HEADERS
FROM 'file:///owns_email.csv'  AS row
MATCH (c:Customer {name: row.Customer})
MATCH (p:Email {email: row.Email})
MERGE (c)-[r:OWNS_EMAIL]->(p);

// CREATE Claim
CREATE CONSTRAINT Claim_claimId IF NOT EXISTS 
FOR (x:Claim) REQUIRE x.claimId IS UNIQUE;

LOAD CSV WITH HEADERS FROM 'file:///claims.csv' AS row
MERGE (c:Claim {claimId: row.ClaimID})
SET
  c.claimId = row.ClaimID,
  c.risk = row.Risk,
  c.admissionDate = date(datetime({epochMillis: apoc.date.parse(row.AdmissionDate, 'ms', 'd-MMM-yy')})),
  c.age=row.Age,
  c.disease = row.Disease,
  c.los = toInteger(row.Los),
  c.fraud = row.Fraud,
  c.narration = row.Narration;
  
  
// Create relationship Customer FILED Claim
LOAD CSV WITH HEADERS
FROM 'file:///filed_claim.csv'  AS row
MATCH (c:Customer {name: row.Customer})
MATCH (clm:Claim {claimId: row.ClaimID})
MERGE (c)-[r:FILED_CLAIM]->(clm);

// Create Claim Embedding
LOAD CSV WITH HEADERS
FROM 'file:///openai_embedding_3small.csv'
AS row
MATCH (c:Claim {claimId: row.ClaimID})
CALL db.create.setNodeVectorProperty(c, 'embedding', apoc.convert.fromJsonList(row.NarrationEmbedding))
RETURN count(*);

// 1536 for ada002 and 3-small, 3072 for 3-large
CALL db.index.vector.createNodeIndex(
    'claimNarration',
    'Claim',
    'embedding',
    1536,
    'cosine'
);


// CREATE Hospital
CREATE CONSTRAINT Hospital_name IF NOT EXISTS 
FOR (x:Hospital) REQUIRE x.name IS UNIQUE;
LOAD CSV WITH HEADERS FROM 'file:///hospitals.csv' AS row
MERGE (c:Hospital {name: row.Hospital})
SET 
	c.name = row.Hospital;
	

// Create relationship Hospital PROVIDED_MEDICAL_SERVICE Claim
LOAD CSV WITH HEADERS
FROM 'file:///provided_medical.csv'  AS row
MATCH (h:Hospital {name: row.Hospital})
MATCH (clm:Claim {claimId: row.ClaimID})
MERGE (h)-[r:PROVIDED_MEDICAL_SERVICE]->(clm);


// CREATE Agent
CREATE CONSTRAINT Agent_name IF NOT EXISTS 
FOR (x:Agent) REQUIRE x.name IS UNIQUE;
LOAD CSV WITH HEADERS FROM 'file:///agents.csv' AS row
MERGE (a:Agent {name: row.Agent})
SET 
	a.name = row.Agent;
	
// Create relationship Agent SERVICED Claim
LOAD CSV WITH HEADERS
FROM 'file:///serviced_claim.csv'  AS row
MATCH (a:Agent {name: row.Agent})
MATCH (clm:Claim {claimId: row.ClaimID})
MERGE (a)-[r:SERVICED_CLAIM]->(clm);