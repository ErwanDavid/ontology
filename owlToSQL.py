from pronto import Ontology
import sqlite3
import pprint as pp
import re, sys, os

ontoFile = os.path.abspath("./owl_file/" + sys.argv[1] + ".owl")
print("Use", ontoFile)
myOnto = Ontology(ontoFile)

conn = sqlite3.connect("onto01.db")


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


termArray = myOnto.terms()
for curTerm in termArray:
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
    if curTerm.xrefs:
        try:
            iterator = map(lambda xref: xref.id, curTerm.xrefs )
            for ref in  list(iterator):
                insertXref(curTerm.id,ref)
        except:
            pass
    


