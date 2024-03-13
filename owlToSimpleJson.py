from pronto import Ontology
import pprint as pp
import re, sys

ontoFile = "/home/erwan/Documents/GIT_PERSO/ontology/owl_file/" + sys.argv[1] + ".owl"
print("Use", ontoFile)
myOnto = Ontology(ontoFile) 
#myOnto = Ontology("/home/erwan/Documents/GIT_PERSO/ontology/owl_file/pw.owl") 

relationArray = list(myOnto.relationships())
for synonym in relationArray:
    print("Found relations type", synonym)

termArray = myOnto.terms()
print("Nbr item", len(termArray))

for curTerm in termArray:
    myTerm = {}
    myTerm['_id'] = curTerm.id
    myTerm['name'] = curTerm.name
    myTerm['namespace'] = curTerm.namespace
    myTerm['definition'] = re.sub(r'[^A-Za-z0-9]+',' ', str(curTerm.definition))
    if curTerm.xrefs:
        try:
            iterator = map(lambda xref: xref.id, curTerm.xrefs )
            myTerm['xrefs'] = list(iterator)
        except:
            pass
    if curTerm.definition:
        try:
            iterator = map(lambda xref: str(xref), curTerm.definition.xrefs )
            iterator2 = map(lambda xref: re.search('\w+:[^\']+', xref).group(), iterator )
            myTerm['definition_xrefs'] = list(iterator2)
        except:
            pass
    if curTerm.synonyms :
        iterator = map(lambda syn: syn.description, curTerm.synonyms )
        #iterator2 = map(lambda xref: re.search('\w+:\w+\-', xref).group(), iterator )
        myTerm['synonyms'] = list(iterator)
    


    if curTerm.relationships : 
        curRel = {}
        try:
            for relTyp in curTerm.relationships.keys():
                curRel["type"] = relTyp.name
            for relVal in curTerm.relationships.values():
                val = relVal.pop()
                curRel["term"] = val.id
                if 'xref' in myTerm.keys():
                    myTerm['xrefs'].append(curRel["term"])
                else:
                    myTerm['xrefs'] = []
                    myTerm['xrefs'].append(curRel["term"])
                curRel["name"] = val.name
        except KeyError:
            print("Error REL on ", curTerm.name, curTerm.relationships)
        myTerm['relation'] = curRel 

    if curTerm.annotations:
        myTerm['annotation'] = curTerm.annotations.pop().property 


    pp.pprint(myTerm)





#with open("myOnto.json", "wb") as f:
#    myOnto.dump(f, format="json")

    #xRefArray = list(term.xrefs)
    #for xRef in xRefArray:
    #    print("   xref", xRef)

    #if myOnto.get_relationship('part_of') in term.relationships.keys():
    #    print("Part_Of", term.relationships[myOnto.get_relationship('part_of')])

