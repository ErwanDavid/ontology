# Testing ontologies and graph database

## Idea
Run test of importing the https://obofoundry.org/ data on different database: sqlite or neo4j. The goal is to allow better understanding of the ontologies structure

## Structure
In the docker folder :

 - a neo4j docker that run a get on the https://neo4j.com/labs/neosemantics/ plugin and a specific config file 
 - a python image that run fastapi to manage different actions on top of the neo4j image
 - a docker compose file

## Code

 - main.py : the fastapi main file
 - other python to be integrated (got owl files, different test using pronto and owlready2
