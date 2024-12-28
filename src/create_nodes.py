import json, sys
import pprint as pp

from py2neo import Graph, Node, Relationship
from py2neo.bulk import create_nodes, create_relationships

neoDriver = Graph("neo4j://localhost:7687")

FILE_IN = sys.argv[1]
OBJ_TYPE = sys.argv[2]
BATCH_S = 1000

entity_keys = ["id", "name", "definition", "synonyms", "annotations"]

print("From ", FILE_IN, "using", OBJ_TYPE)

def splice_array(bigArray, start, step):
    stop = start + step
    ret_array = bigArray[start:stop]
    return ret_array

def getEntity():
    tmp_array = []
    with open(FILE_IN) as f:
        for line in f:
            cur_entity = json.loads(line)
            #pp.pprint(cur_entity)
            tmp_ent = []
            for need_key in entity_keys:
                if need_key in cur_entity.keys():
                    if need_key == 'synonyms':
                        cur_entity[need_key].append(cur_entity['name'])
                        cur_entity[need_key] = ','. join(cur_entity[need_key])
                    if need_key == 'annotations':
                        cur_entity[need_key] = str(cur_entity[need_key])
                    tmp_ent.append(cur_entity[need_key])
            tmp_array.append(tmp_ent)
    return tmp_array

def createEntity(ListGrp):
    tot_len = len(ListGrp)
    cur_pos = 0
    while tot_len > 0:
        cur_arr = splice_array(ListGrp, cur_pos, BATCH_S)
        print("Batch insert", cur_pos,tot_len)
        cur_pos = cur_pos + BATCH_S
        tot_len = tot_len - BATCH_S
        create_nodes(neoDriver.auto(), cur_arr, labels={OBJ_TYPE}, keys=entity_keys)


createEntity(getEntity())


