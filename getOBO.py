from urllib.request import urlopen
import urllib.request
import json
#import pandas as pd
import pprint as pp

response = urlopen("https://obofoundry.org/registry/ontologies.jsonld")
ontologyListJson = response.read()
ontologyList = json.loads(ontologyListJson)['ontologies']
#pp.pprint(ontologyList)
# http://purl.obolibrary.org/obo/pw.owl'

#importantOnto = ['bfo','cob','clo','bto','pw','chebi','doid','dron']
importantOnto = ['pw','dron']

for onto in ontologyList:
    if onto['id'] in importantOnto :
        print("Find ",onto['id'], "title",onto['title'])
        for product in onto['products']:
            idStr = './owl_file/' + onto['id'] + ".owl"
            if product['id'] == onto['id'] + ".owl" :
                print("DL OWL URL", product['ontology_purl'])
                urllib.request.urlretrieve(product['ontology_purl'], idStr)
                print("")
