import gpt


planmap = {
    'layers': {
        'geologic_units': {
            'columns': ['name','rgb','geo_type','geo_code'],
            'geometry': 'Polygon'
        },
        'geologic_contacts': {
            'columns': ['geo_type'],
            'geometry': 'Linestring'
        },
        'surface_features': {
            'columns': ['geo_type'],
            'geometry': 'Polygon'
        },
        'linear_features': {
            'columns': ['geo_type'],
            'geometry': 'Linestring'
        },
        'layer_styles': {
            'columns': ['styleQML','styleSLD']
        }
    }
}

def check_layer_names(pkg, layers):
    """
    Return True/False if all 'layers' were found/not

    Args:
        pkg: Geopkg
        layers: List[str]
            List of layer names expected to be found
    """
    out = []

    pl = set(pkg.keys())
    el = set(layers)

    layers_found = el.intersection(pl)
    layers_extra = pl.difference(el)
    layers_notfound = el.difference(layers_found)

    print("Expected layers:", list(layers))
    print("Layers found:", list(layers_found))
    print("Layers not found:", list(layers_notfound))
    print("Extra layers:", list(layers_extra))

    # Return True if all required layers were found
    return len(layers_notfound) == 0


def _check_if_sets_match(values_have, values_expected):
    """
    Return (notfound,extra) sets of "not-found" and "extra" values

    Args:
        values_have: List[str]
            Set/list of values we have at hand
        values_expected: List[str]
            Set/list of values we expect to find
    """
    have = set(values_have)
    expect = set(values_expected)

    found = expect.intersection(have)
    notfound = expect.difference(found)
    extra = have.difference(expect)

    return (notfound, extra)


def check_field_names(pkg, layer_columns, case_insensitive=False):
    """
    Return True/False if all columns were found/not in respective layer(s)

    Args:
        pkg: Geopkg
        layer_columns: Dict[str, List[str]]
            Dictionary providing columns names (values) for each layer (key)
    """
    for layer,columns in layer_columns.items():
        assert layer in pkg, "Layer '{}' not found in pkg".format(layer)

        notfound, extra = _check_if_sets_match(pkg[layer].columns, columns)

        if len(notfound):
            print("Columns {} not found in layer {}".format(notfound,layer))

    return len(notfound) == 0


def check_geometry(pkg):
    """
    Return True/False if geometry columns has some nulls/not

    If _all_ values of a geometry column are Null, it's ok (case of 'layer_styles').
    But if _some_ values are Null, it's not ok, return False.

    Args:
        pkg: Geopkg
    """
    ok = True
    for layer, df in pkg.layers:
        geometry_bool = df['geometry'].isnull()
        if all(geometry_bool):
            print("All values of 'geometry' from layer '{}' are Null.".format(layer))
            continue
        if any(geometry_bool):
            print("Found Null geometries in layer {}:".format(layer))
            print(df[geometry_bool])
            ok = False

    return ok


def check_crs(pkg):
    """
    Return True if only one CRS is found, False if multiple were found
    """
    CRSs = dict()
    for lname, df in pkg.layers:
        crs = df.crs
        # - 'layer_styles' (by QGIS) has no 'geometry'
        # - accumulate crs(s) in a hash to check later for heterogeneity (multiple crs's)
        if lname != 'layer_styles':
            lcrs = CRSs.get(crs, [])
            lcrs.append(lname)
            CRSs[crs] = lcrs

    # - if more than one crs was found, say it
    if len(CRSs) > 1:
        print('Multiple CRSs found')
    # For each crs (hopefully, one), print it (WKT)
    for crs,lrs in CRSs.items():
        print(crs.to_string())

    return len(CRSs) == 1


def geopackage(gpkg):
    """
    Checks to be done:
    - check layer names
    - check column names
    - check if any geometry entry is null, unless all of them are null
    - check if all CRS are equal (for table layers with geometry)
    - check if there are multiple "shape" and "id" columns
    """
    pkg = gpt.read_file(gpkg)
    # # make it "case insensitive" (lower the keys)
    # for lname in list(pkg.keys()):
    #     pkg[lname.lower()] = pkg[lname]
    #     del pkg[lname]

    # Check layer names
    layers_defs = planmap['layers']
    layer_columns = {l:defs['columns'] for l,defs in layers_defs.items()}

    ok = check_layer_names(pkg, layers_defs.keys())
    ok *= check_field_names(pkg, layer_columns)
    ok *= check_geometry(pkg)
    ok *= check_crs(pkg)
