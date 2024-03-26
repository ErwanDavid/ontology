from neo4j import GraphDatabase

URI = "neo4j://myneo/"

with GraphDatabase.driver(URI) as driver:
    driver.verify_connectivity()
    with driver.session(database="neo4j") as session:
        # CREATE CONSTRAINT
        try:
            session.run("CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE")
        except:
            pass
        # Init graph
        try:
            session.run("CALL n10s.graphconfig.init({  handleVocabUris: 'MAP'})")
        except:
            pass
        #importantOnto = ['bfo','ado','duo','proco','cob','clo','bto','dideo','pw','chebi','doid','dron', 'ncbitaxon', 'uberon', 'ro', 'chiro']
        importantOnto = ['ado','duo','proco','cob','clo','bto','dideo','pw','doid','dron', 'uberon', 'ro', 'chiro']
        urlRoot = 'https://purl.obolibrary.org/obo/'
        for onto in importantOnto:
            print('onto', onto)
            session.run("CALL n10s.rdf.import.fetch('" + urlRoot +  onto + "','RDF/XML')")
            


        print("ok")




