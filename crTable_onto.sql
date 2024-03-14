CREATE TABLE entity (
	id TEXT,
	name TEXT,
	definition TEXT,
	definition_ref TEXT,
	namespace TEXT,
	CONSTRAINT entity_PK PRIMARY KEY (id)
);

CREATE TABLE synonyms (
	main_ID TEXT,
	syn_name TEXT,
	CONSTRAINT synonyms_FK FOREIGN KEY (main_ID) REFERENCES entity(id)
);

CREATE TABLE xrefs (
	main_ID TEXT,
	xref_ID TEXT,
	CONSTRAINT xrefs_FK FOREIGN KEY (main_ID) REFERENCES entity(id)
);

CREATE TABLE relations (
	main_ID TEXT,
	related_ID TEXT,
	related_name TEXT,
	relation_name TEXT,
	CONSTRAINT relations_FK FOREIGN KEY (main_ID) REFERENCES entity(id)
);