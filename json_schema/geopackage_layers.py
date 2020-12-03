
_component = __file__.split('.')[0]
_schemafile = '.'.join([_component, 'schema', 'json'])

with open(_schemafile) as f:
    import json
    schema = json.load(f)

def validate(gpkg_path):
    import fiona
    data = fiona.listlayers(gpkg_path)

    import jsonschema
    res = jsonschema.validate(data, schema)

    return res
