from pronto import Ontology
import pprint as pp
import re, sys, os, json

ontoFile = os.path.abspath("./owl_file/" + sys.argv[1] + ".owl")
resultFile = os.path.abspath("./owl_file/" + sys.argv[1] + ".res.json")
print("From ", ontoFile)
print("To ", resultFile)
myOnto = Ontology(ontoFile, threads=1) 

resFile = open(resultFile, "w") 

annot_conf = {
 'http://purl.obolibrary.org/obo/BFO_0000179': 'BFO OWL label',
 'http://purl.obolibrary.org/obo/BFO_0000180': 'BFO CLIF label',
 'http://purl.obolibrary.org/obo/IAO_0000112': 'Examples',
 'http://purl.obolibrary.org/obo/IAO_0000111': 'IAO_0000111',
 'http://purl.obolibrary.org/obo/IAO_0000114': 'IAO_0000114',
 'http://purl.obolibrary.org/obo/IAO_0000117': 'IAO_0000117',
 'http://purl.obolibrary.org/obo/IAO_0000231': 'IAO_0000231',
 'http://purl.obolibrary.org/obo/IAO_0000116': 'Editor note',
 'http://purl.obolibrary.org/obo/IAO_0000118': 'Alternative label',
 'http://purl.obolibrary.org/obo/IAO_0000119': 'Definition src',
 'http://purl.obolibrary.org/obo/IAO_0000232': 'IAO_0000232',
 'http://purl.obolibrary.org/obo/IAO_0000233': 'IAO_0000233',
 'http://purl.obolibrary.org/obo/IAO_0000589' : 'IAO_0000589',
 'http://purl.obolibrary.org/obo/RO_0002175': 'RO_0002175',
 'http://purl.obolibrary.org/obo/RO_0002604': 'Opposite',
 'http://purl.obolibrary.org/obo/RO_0002161': 'RO_0002161',
 'http://purl.obolibrary.org/obo/IAO_0006012': 'IAO_0006012',
 'http://purl.obolibrary.org/obo/IAO_0000600': 'Elucidation',
 'http://purl.obolibrary.org/obo/IAO_0000601': 'Has axiom',
 'http://purl.obolibrary.org/obo/IAO_0000602': 'Has axiom',
 'http://www.w3.org/2000/01/rdf-schema#isDefinedBy': 'isDefineBy',
 'http://purl.obolibrary.org/obo/IAO_0000231': 'IAO_0000231',
 'http://purl.obolibrary.org/obo/chebi/charge': 'charge',
 'http://purl.obolibrary.org/obo/chebi/formula': 'formula',
 'http://purl.obolibrary.org/obo/chebi/inchi': 'inchi',
 'http://purl.obolibrary.org/obo/chebi/inchikey': 'inchikey',
 'http://purl.obolibrary.org/obo/chebi/mass': 'mass',
 'http://purl.obolibrary.org/obo/chebi/monoisotopicmass': 'monoisotopicmass',
 'http://purl.obolibrary.org/obo/OBI_9991118': 'IEDB alternative term',
#  'http://purl.obolibrary.org/obo/mondo#curated_content_resource': 'curated_content_resource',
#  'http://purl.obolibrary.org/obo/mondo#excluded_from_qc_check': 'excluded_from_qc_check',
#  'http://purl.obolibrary.org/obo/mondo#excluded_subClassOf': 'excluded_subClassOf',
#  'http://purl.obolibrary.org/obo/mondo#should_conform_to': 'should_conform_to',
#  'http://www.w3.org/2004/02/skos/core#broadMatch': 'broadMatch',
#  'http://www.w3.org/2004/02/skos/core#closeMatch': 'closeMatch',
#  'http://www.w3.org/2004/02/skos/core#exactMatch': 'exactMatch',
#  'http://www.w3.org/2004/02/skos/core#narrowMatch': 'narrowMatch',
#  'http://www.w3.org/2004/02/skos/core#relatedMatch': 'relatedMatch',
 'http://www.w3.org/2000/01/rdf-schema#seeAlso': 'seeAlso',
 'https://w3id.org/semapv/vocab/crossSpeciesExactMatch' : 'crossSpeciesExactMatch',
 'http://xmlns.com/foaf/0.1/depiction' : 'depiction',
 'http://purl.obolibrary.org/obo/chebi/smiles': 'smiles'}

relationArray = list(myOnto.relationships())
for relationType in relationArray:
    print("Found relations type", relationType)


synArray = myOnto.synonym_types()
for synonym in synArray:
    print("Found synonyms type", synonym)


termArray = myOnto.terms()
print("* * * Nbr item", len(termArray))


distinct_annot = {}
distinct_xrefs = {}


for curTerm in termArray:
    myTerm = {}
    #pp.pprint(curTerm)
    print("_________", curTerm.id)
    # IDs
    myTerm['id'] = curTerm.id
    myTerm['name'] = curTerm.name
    if curTerm.namespace:
        myTerm['namespace'] = curTerm.namespace

    # Definition
    if curTerm.definition:
        myTerm['definition'] = re.sub(r'[^A-Za-z0-9\.\,]+',' ', str(curTerm.definition))

    # xrefs
    if curTerm.xrefs:
        try:
            iterator = map(lambda xref: xref.id, curTerm.xrefs )
            myTerm['xrefs'] = list(iterator)
        except:
            pass

    # Definition xrefs
    if curTerm.definition:
        try:
            iterator = map(lambda xref: str(xref), curTerm.definition.xrefs )
            iterator2 = map(lambda xref: re.search('\w+:[^\']+', xref).group(), iterator )
            myTerm['definition_xrefs'] = list(iterator2)
        except:
            pass
    
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
        except KeyError  as e:
            #print("Error on", curTerm.name, curTerm.id, e.args[0])
            curRel["type"] = e.args[0]
        pp.pprint(curRel)
        # try:
        #     for existRel in relationArray:
        #         print("REL2",  curTerm.name, curTerm.id, existRel, curTerm.relationships.pop(existRel))
        # except  KeyError as e: 
        #     print("Error on", curTerm.name, curTerm.id, e.args[0])
        # try:
        #     relSet = list(curTerm.relationships) #.items()
        #     for rel in relSet:
        #         print("RELATION :", rel)
        # except  KeyError as e: 
        #    print("Error on ", curTerm.name, curTerm.relationships, e.args[0])
        myTerm['curRel'] = curRel 

    if curTerm.annotations:
        annot_array = []
        for myAnnot in curTerm.annotations:
            tmp_dic = {}
            if myAnnot.property in annot_conf.keys():
                annot_name = annot_conf[myAnnot.property]
            else:
                if '#' in myAnnot.property:
                    annot_name = myAnnot.property.split('#')[-1]
                else:
                    annot_name = myAnnot.property.split('/')[-1]
            #annot_name = myAnnot.property
            tmp_dic[annot_name] = 1
            try:
                tmp_dic[annot_name] = myAnnot.literal
            except:
                tmp_dic[annot_name] = myAnnot.resource
            annot_array.append(tmp_dic)
            if myAnnot.property in distinct_annot.keys():
                distinct_annot[myAnnot.property] += 1
            else:
                distinct_annot[myAnnot.property] = 1
        myTerm['annotations'] = annot_array
    
    if curTerm.disjoint_from: 
        disjoint_array = []
        for myDis in curTerm.disjoint_from:
            tmp = {}
            tmp['id'] = myDis.id
            tmp['name'] = myDis.name
            disjoint_array.append(tmp)
        myTerm['disjoint_from'] = disjoint_array
    
    if curTerm.superclasses :
        sub = iter(curTerm.superclasses())
        term = next(sub)
        try:
            term = next(sub)
        except:
            myTerm['isRoot'] = 'Yes'
            pass #print('root')
        tmp = {}
        tmp['id'] = term.id
        tmp['name'] = term.name
        myTerm['superclasses'] = tmp
    
    if curTerm.synonyms :
        syn_arr = []
        for mySyn in curTerm.synonyms:
            syn_arr.append(mySyn.description)
        myTerm['synonyms'] = syn_arr

    # Distinct xrefs ontologies
    if 'xrefs' in myTerm.keys() : 
        for xref in myTerm['xrefs']:
            ontology = xref.split(':')[0]
            if ontology in distinct_xrefs.keys():
                distinct_xrefs[ontology] += 1
            else:
                distinct_xrefs[ontology] = 1

    if sys.argv[1] in myTerm['id'].lower() : 
        print(json.dumps(myTerm), file=resFile)

pp.pprint(distinct_annot)
pp.pprint(distinct_xrefs)


resFile.close()