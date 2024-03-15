from pronto import Ontology
import sqlite3
import pprint as pp
import re, sys, os

ontoFile = os.path.abspath("./owl_file/" + sys.argv[1] + ".owl")
print("Use", ontoFile)
myOnto = Ontology(ontoFile)

conn = sqlite3.connect("onto01.db")
<<<<<<< HEAD
# require the table from crTable_onto.sql to exist

def insertEntity(ID, name, ns, definition, definition_ref):
    entitySet = (ID, name, ns, definition, definition_ref)
    sql = ''' INSERT or IGNORE INTO entity(id,name, namespace, definition, definition_ref)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entitySet)
    conn.commit()

def insertXref(mainID, refID):
    xrefSet=(mainID, refID)
    sql = ''' INSERT INTO xrefs(main_ID,xref_ID)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, xrefSet)
    conn.commit()


def insertRelation(mainID, curType, curName, curID):
    relationSet=(mainID, curType, curName, curID)
    sql = ''' INSERT INTO relations (main_ID, related_ID, related_name, relation_name)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, relationSet)
    conn.commit()

def insertSyn(mainID, synName):
    synSet=(mainID, synName)
    sql = ''' INSERT INTO synonyms(main_ID,syn_name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, synSet)
    conn.commit()
=======


def insertEntity(ID, name, ns, definition, definition_ref):
    entitySet = (ID, name, ns, definition, definition_ref)
    sql = ''' INSERT INTO entity(id,name, namespace, definition, definition_ref)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entitySet)
    conn.commit()

def insertXref(mainID, refID):
    xrefSet=(mainID, refID)
    sql = ''' INSERT INTO xref(main_ID,xref_ID)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, xrefSet)
    conn.commit()

>>>>>>> e9e590a6abc5d8d93e14174ec34f14b9b75ebb15

termArray = myOnto.terms()
for curTerm in termArray:
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
    insertEntity(curTerm.id, curTerm.name, curTerm.namespace, definition, definition_ref)
<<<<<<< HEAD
    # xrefs
    if curTerm.xrefs:
        try:
            iterator = map(lambda xref: xref.id, curTerm.xrefs )
            for ref in iterator:
                insertXref(curTerm.id,ref)
        except:
            pass
    # Synonymes
    if curTerm.synonyms :
        iterator = map(lambda syn: syn.description, curTerm.synonyms )
        #iterator2 = map(lambda xref: re.search('\w+:\w+\-', xref).group(), iterator )
        for curSyn in iterator:
            insertSyn(curTerm.id,curSyn)
    
    if curTerm.relationships : 
        try:
            curType = curID = curName = ''
            for relTyp in curTerm.relationships.keys():
                curType = relTyp.name
            for relVal in curTerm.relationships.values():
                val = relVal.pop()
                curID = val.id
                curName = val.name
                insertRelation(curTerm.id, curType, curName, curID)
        except KeyError:
            print("Error REL on ", curTerm.name, curTerm.relationships)
            
=======
    if curTerm.xrefs:
        try:
            iterator = map(lambda xref: xref.id, curTerm.xrefs )
            for ref in  list(iterator):
                insertXref(curTerm.id,ref)
        except:
            pass
    


>>>>>>> e9e590a6abc5d8d93e14174ec34f14b9b75ebb15
