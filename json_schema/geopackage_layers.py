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

    # print("\nGeoPackage layers/columns:")
    # for name,table in gpkg.layers:
    #     print(name)
    #     print(table.columns)
    #     print()

    # This is a workaround during devel, until I understand how to tell jsonschema about the DataFrames
    data = {ln:{} for ln in gpkg.list()}
    data['layer_styles']['geometry'] = list(gpkg['layer_styles']['geometry'].values)
    data['layer_styles']['geometry'] = []
    # print(data)

    import jsonschema
    res = jsonschema.validate(data, schema)

    return res
