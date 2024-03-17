from owlready2 import *
import pprint as pp

onto = get_ontology("file:///home/erwan/Documents/GIT_PERSO/ontology/owl_file/doid.owl").load()



print("Comments", onto.metadata.comment)
print("List classes")
pp.pprint(list(onto.classes()))
default_world.set_backend(filename = "doid.sqlite3")
default_world.save()