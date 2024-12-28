


import json, sys
import pprint as pp

from py2neo import Graph, Node, Relationship
from py2neo.bulk import create_nodes, create_relationships

neoDriver = Graph("neo4j://localhost:7687")

FILE_IN = sys.argv[1]
OBJ_TYPE = sys.argv[2]
BATCH_S = 1000

print("From ", FILE_IN, "using", OBJ_TYPE)

def splice_array(bigArray, start, step):
    stop = start + step
    ret_array = bigArray[start:stop]
    return ret_array

def getRelationsSuperclasse():
    ret_arr = []
    with open(FILE_IN) as f:
        for line in f:
            cur_entity = json.loads(line)
            if 'superclasses' in cur_entity.keys():
                newrel = []
                newrel.append(cur_entity['id'])
                map = {'comment' : 'test'}
                newrel.append(map)
                newrel.append(cur_entity['superclasses']['id'])
                ret_arr.append(newrel)
    return ret_arr

def getRelationsXrefs():
    ret_arr = []
    with open(FILE_IN) as f:
        for line in f:
            cur_entity = json.loads(line)
            if 'xrefs' in cur_entity.keys():
                for term in cur_entity['xrefs'] :
                    newrel = []
                    newrel.append(cur_entity['id'])
                    map = {'comment' : 'test'}
                    newrel.append(map)
                    newrel.append(term)
                    ret_arr.append(newrel)
    return ret_arr


def createRelation(ListRel, name):
    tot_len = len(ListRel)
    cur_pos = 0
    rel_batch = int(BATCH_S / 1)
    while tot_len > 0:
        cur_arr = splice_array(ListRel, cur_pos, rel_batch)
        print("Batch insert Relation", cur_pos,tot_len)
        cur_pos = cur_pos + rel_batch
        tot_len = tot_len - rel_batch
        create_relationships(neoDriver.auto(), cur_arr, name, start_node_key=(OBJ_TYPE, "id"), end_node_key=(OBJ_TYPE, "id"))


createRelation(getRelationsSuperclasse(), 'superclasses')
createRelation(getRelationsXrefs(), 'xrefs')

