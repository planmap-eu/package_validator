import jsonschema
import json

_component = __file__.split('.')[0]
_schemafile = '.'.join([_component, 'schmea', 'json'])

def validate(geopackage):
    import fiona
    with open(_schemafile) as f:
        schema = json.load(_schemafile)

    data = fiona.listlayers(geopackage)
    res = jsonschema.validate(data, schema)
