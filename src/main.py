from fastapi import FastAPI
from urllib.request import urlopen
import urllib.request
import json
import os

app = FastAPI()


response = urlopen("https://obofoundry.org/registry/ontologies.jsonld")
ontologyListJson = response.read()
ontologyList = json.loads(ontologyListJson)['ontologies']

@app.get('/')
def read_root():
    return {"Hello": "World"}


@app.get('/list_owl')
def list_owl():
    return os.listdir("/code/owl_file/")

@app.get('/add_owl/{onto_code}')
def add_owl(onto_code):
    return {"add_owl": onto_code}