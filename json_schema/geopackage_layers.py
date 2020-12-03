import gpt

_component = __file__.split('.')[0]
_schemafile = '.'.join([_component, 'schema', 'json'])

with open(_schemafile) as f:
    import json
    schema = json.load(f)

def validate(gpkg_path):
    # import fiona
    # data = fiona.listlayers(gpkg_path)
    gpkg = gpt.read_file(gpkg_path)

    # This is a workaround during devel, until I understand how to tell jsonschema about the DataFrames
    data = {ln:ln for ln in gpkg.list()}

    import jsonschema
    res = jsonschema.validate(data, schema)

    return res
