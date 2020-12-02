"""
Get a package path and check its content.

The package content checking is processed by a series/pipeline of tasks
on specific request or automatically (if None asked) after parsing/interpreting
the package name, or greedly inpecting any of the expected directories.
"""
import os
import sys
import pytest

import gpt
import check


_data = {
    'gpkg': None,
    'schema': None
}

# def find_gpkg(pkg_path):
#     pkg_name = os.path.basename(os.path.abspath(pkg_path))
#     pkg_specs = parse_package_name(pkg_name)
#     pkg_specs['name'] = pkg_name
#     return os.path.join(pkg_path, 'vector', pkg_specs['name']+'.gpkg')

@pytest.fixture()
def geopkg_path(pytestconfig):
    return pytestconfig.getoption('pkgpath')

@pytest.fixture()
def schema_name(pytestconfig):
    return pytestconfig.getoption('schema')

@pytest.fixture()
def gpkg():
    return _data['gpkg']

@pytest.fixture()
def schema():
    return _data['schema']

@pytest.fixture()
def layer_names():
    layers_defs = _data['schema']['layers']
    return layers_defs.keys()

@pytest.fixture()
def layers_columns():
    layers_defs = _data['schema']['layers']
    return {l:defs['columns'] for l,defs in layers_defs.items()}


def test_00(geopkg_path, schema_name):
    assert os.path.exists(geopkg_path), "Geopackage file/path NOT found."
    gpkg = gpt.read_file(geopkg_path)
    assert gpkg, "Geopackage is apparently empty/null."
    _data['gpkg'] = gpkg
    print("\nGeopackage loaded ({})".format(geopkg_path))
    import schema
    gpkg_schema = getattr(schema,schema_name)
    _data['schema'] = gpkg_schema


def test_layer_names(gpkg, layer_names):
    print("\n* Layer names")
    res = check.check_layer_names(gpkg, layer_names)
    assert res is True

def test_field_names(gpkg, layers_columns):
    print("\n* Field names")
    res = check.check_field_names(gpkg, layers_columns)
    assert res is True

def test_geometry(gpkg):
    res = check.check_geometry(gpkg)
    assert res is True

def test_crs(gpkg):
    res = check.check_crs(gpkg)
    assert res is True
