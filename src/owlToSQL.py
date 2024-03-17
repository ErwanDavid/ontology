from pronto import Ontology
import sqlite3
import pprint as pp
import re, sys, os

ontoFile = os.path.abspath("./owl_file/" + sys.argv[1] + ".owl")
print("Use", ontoFile)
myOnto = Ontology(ontoFile)

conn = sqlite3.connect("data_file/onto02.db")
# require the table from crTable_onto.sql to exist

def execAnCommit(sql, dataset, doCommit):
    cur = conn.cursor()
    cur.execute(sql, dataset)
    if doCommit:
        conn.commit()


def insertEntity(ID, name, ns, definition, definition_ref,doCommit):
    entitySet = (ID, name, ns, definition, definition_ref)
    sql = ''' INSERT or IGNORE INTO entity(id,name, namespace, definition, definition_ref)
              VALUES(?,?,?,?,?) '''
    execAnCommit(sql, entitySet,doCommit)


def insertXref(mainID, refID,doCommit):
    xrefSet=(mainID, refID)
    sql = ''' INSERT INTO xrefs(main_ID,xref_ID)
              VALUES(?,?) '''
    execAnCommit(sql, xrefSet,doCommit)


def insertRelation(mainID, curType, curName, curID,doCommit):
    relationSet=(mainID, curType, curName, curID)
    sql = ''' INSERT INTO relations (main_ID, related_ID, related_name, relation_name)
              VALUES(?,?,?,?) '''
    execAnCommit(sql, relationSet,doCommit)

def insertSyn(mainID, synName,doCommit):
    synSet=(mainID, synName)
    sql = ''' INSERT INTO synonyms(main_ID,syn_name)
              VALUES(?,?) '''
    execAnCommit(sql, synSet,doCommit)

termArray = myOnto.terms()
doCommit = False
cpt = 0
for curTerm in termArray:
    cpt += 1
    if cpt > 100:
        print('+')
        doCommit = True
        cpt = 0
    else:
        doCommit = False
    # Main entity # Todo : obsolet flag 
    definition = re.sub(r'[^A-Za-z0-9\.\,]+',' ', str(curTerm.definition))
    definition_ref = ''
    if curTerm.definition:
        try:
            iterator = map(lambda xref: str(xref), curTerm.definition.xrefs )
            iterator2 = map(lambda xref: re.search('\w+:[^\']+', xref).group(), iterator )
            defition_ref = ' '.join(list(iterator2))
        except:
            pass
    insertEntity(curTerm.id, curTerm.name, curTerm.namespace, definition, definition_ref, doCommit)
    # xrefs
    if curTerm.xrefs:
        try:
            iterator = map(lambda xref: xref.id, curTerm.xrefs )
            for ref in iterator:
                insertXref(curTerm.id, ref, doCommit)
        except:
            pass
    # Synonymes
    if curTerm.synonyms :
        iterator = map(lambda syn: syn.description, curTerm.synonyms )
        #iterator2 = map(lambda xref: re.search('\w+:\w+\-', xref).group(), iterator )
        for curSyn in iterator:
            insertSyn(curTerm.id, curSyn, doCommit)
    
    if curTerm.relationships : 
        try:
            curType = curID = curName = ''
            for relTyp in curTerm.relationships.keys():
                curType = relTyp.name
            for relVal in curTerm.relationships.values():
                val = relVal.pop()
                curID = val.id
                curName = val.name
                insertRelation(curTerm.id, curType, curName, curID, doCommit)
        except KeyError:
            print("Error REL on ", curTerm.name, curTerm.relationships)
            
