from fastapi import FastAPI
from urllib.request import urlopen
import urllib.request
import json
import os, time 
from neo4j import GraphDatabase

URI = "neo4j://myneo/"

app = FastAPI()

time.sleep(20)

response = urlopen("https://obofoundry.org/registry/ontologies.jsonld")
ontologyListJson = response.read()
ontologyList = json.loads(ontologyListJson)['ontologies']
                 


@app.get('/')
def read_root():
    return {"Hello": "World"}


@app.get('/init_db')
def init_db():
        with GraphDatabase.driver(URI) as driver:
            driver.verify_connectivity()
            with driver.session(database="neo4j") as session:
                session.run("CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE")
                session.run("CALL n10s.graphconfig.init({ handleVocabUris: 'MAP'})")  
                #session.run("CALL n10s.graphconfig.init({ handleRDFTypes:'LABELS_AND_NODES'});")  
        return {"init": "Done"}
             

@app.get('/add_owl/{onto_code}')
def add_owl(onto_code):
        with GraphDatabase.driver(URI) as driver:
            driver.verify_connectivity()
            with driver.session(database="neo4j") as session:
                for onto in ontologyList:
                    if onto['id'] == onto_code :
                        print("Find ",onto['id'], "title",onto['title'])
                        for product in onto['products']:
                            if product['id'] == onto['id'] + ".owl" :
                                print("DL OWL URL", product['ontology_purl'])
                                session.run("CALL n10s.rdf.import.fetch('" + product['ontology_purl']+ "','RDF/XML')")
        return {"added_owl": onto_code}

@app.get('/delnolabel_owl')
def delnolabel_owl():
     with GraphDatabase.driver(URI) as driver:
            driver.verify_connectivity()
            with driver.session(database="neo4j") as session:
                session.run("MATCH (n:Resource) where n.label is null CALL { WITH n DETACH DELETE n} IN TRANSACTIONS OF 10000 ROWS")
                return {"remove": "done"}

@app.get('/updatenode')
def updatenode():
     total = 0
     with GraphDatabase.driver(URI) as driver:
            driver.verify_connectivity()
            with driver.session(database="neo4j") as session:
                result = session.run("MATCH (n:Resource) where n.hasOBONamespace is not null  WITH DISTINCT n.hasOBONamespace AS NS, collect(DISTINCT n) AS onto  CALL apoc.create.addLabels(onto, [apoc.text.upperCamelCase(NS)]) YIELD node RETURN count(*)")
                total = result.single()[0]
                print('res', total)
                return {"number": total}

@app.get('/countnode')
def countnode():
     with GraphDatabase.driver(URI) as driver:
            driver.verify_connectivity()
            with driver.session(database="neo4j") as session:
                result = session.run("MATCH (n) RETURN count(n)")
                total = result.single()[0]
                print('res', total)
                return {"number": total}


# MATCH (n1:Resource {label: 'heart disease'})-[r]-(n2) RETURN r, n1, n2 LIMIT 25
# MATCH (n) where n.label =~ 'heart.*' return n.label, n
# MATCH (n1)-[r]->(n2) WHERE n1.hasOBONamespace is not null  RETURN r, n1, n2 LIMIT 25
            

