select resources.storid, resources.iri, resources_obo.iri, datas.o,  resources_obo.storid
from datas, resources, resources_obo
where resources_obo.storid = datas.p
and datas.s = resources.storid
order by 2, 3


drop view resources_obo

create view resources_obo as select * from resources where (iri like '%oboInOwl%' or iri like '%rdf-schema%' or iri like '%owl#%' or iri like '%part_of%' or iri like '%IAO%')