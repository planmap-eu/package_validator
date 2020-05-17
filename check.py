import gpt

def check_layer_names(pkg):
    """
    Some layers are mandatory, others are commonly used, but not necessarily.
    """
    out = []
    _mandatory = ['geologic_units',
                  'layer_styles']
    _common = ['geologic_contacts',
               'linear_features',
               'surface_features']

    # check for the mandatory one
    if not all(l in pkg for l in _mandatory):
        out.append("Mandatory layers {!s} not found.".format(_mandatory))

    # check for the commonly used.
    # Extra layers -- not in _mandatory neither in _common -- can be used,
    # which makes the checking for optional layers a bit will defined.
    # What we can do here is to check for if there are many layers and *warn*
    # the user if these _common ones are not there.
    if len(pkg) >= len(_mandatory + _common):
        if not all(l in pkg for l in _common):
            # The cool thing to do here is to have their geometry inspected
            # to have a clue on layer/content match
            msg = "Expected to see layers {!s}".format(_common)
            out.append(msg)

    return out

LAYER_DEFS = dict(
    geologic_units = {'columns': ['name','rgb','geo_type','geo_code'],
                      'geometry': 'Polygon'},
    geologic_contacts = {'columns': ['geo_type'],
                         'geometry': 'Linestring'},
    surface_features = {'columns': ['geo_type'],
                        'geometry': 'Polygon'},
    linear_features = {'columns': ['geo_type'],
                       'geometry': 'Linestring'},
    layer_styles = {'columns': ['styleQML','styleSLD']}
)

def check_field_names(pkg, case_insensitive=False):
    out = []
    for _layer,_defs in LAYER_DEFS.items():
        if _layer not in pkg:
            msg = "Layer {} not found in pkg".format(_layer)
            out.append(msg)
            continue

        if case_insensitive:
            _check_columns = lambda c: c not in pkg[_layer].lower()
        else:
            _check_columns = lambda c: c not in pkg[_layer]
        not_found = list(filter(_check_columns, _defs['columns']))
        if len(not_found):
            msg = "Columns {} not found in layer {}".format(not_found,_layer)
            out.append(msg)

    return out

def check_geometry(pkg):
    """
    Check if geometry has nulls
    """
    out = []
    for lname, df in pkg.layers():
        geometry_bool = df['geometry'].isnull()
        if all(geometry_bool):
            continue
        if any(geometry_bool):
            msg = ("Found null geometries in layer {}\n{}"
                   .format(lname,df[geometry_bool]))
            out.append(msg)

    return out

def check_crs(pkg):
    out = []
    CRSs = dict()
    for lname, df in pkg.layers():
        crs = df.crs
        # - 'layer_styles' (by QGIS) has no 'geometry'
        # - accumulate crs(s) in a hash to check later for heterogeneity (multiple crs's)
        if lname != 'layer_styles':
            lcrs = CRSs.get(crs, [])
            lcrs.append(lname)
            CRSs[crs] = lcrs

    # - if more than one crs was found, say it
    if len(CRSs) > 1:
        out.append('Multiple CRSs found')

    # For each crs (hopefully, one), print it (WKT)
    for crs,lrs in CRSs.items():
        out.append(crs.to_string())

    return out

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
    res = check_layer_names(pkg)
    res += check_field_names(pkg)
    res += check_geometry(pkg)
    res += check_crs(pkg)
    for r in res:
        print(r)
