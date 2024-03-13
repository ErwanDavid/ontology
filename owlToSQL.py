from pronto import Ontology
import sqlite3
import pprint as pp
import re, sys, os

ontoFile = os.path.abspath("./owl_file/" + sys.argv[1] + ".owl")
print("Use", ontoFile)
myOnto = Ontology(ontoFile)


def insertEntity():
    pass

termArray = myOnto.terms()
for curTerm in termArray:
    definition = re.sub(r'[^A-Za-z0-9\.\,]+',' ', str(curTerm.definition))
    insertEntity(curTerm.id,curTerm.name, curTerm.namespace, definition)


