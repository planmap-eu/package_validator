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
    'gpkg': None
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
def gpkg():
    return _data['gpkg']

def test_00(geopkg_path):
    assert os.path.exists(geopkg_path), "Geopackage file/path NOT found."
    gpkg = gpt.read_file(geopkg_path)
    assert gpkg
    _data['gpkg'] = gpkg

# def test_geopackage():
#     out = check.geopackage(_data['gpkg'])

def test_layer_names(gpkg):
    res = check.check_layer_names(gpkg)
    assert res

def test_field_names(gpkg):
    res = check.check_field_names(gpkg)
    assert res

def test_geometry(gpkg):
    res = check.check_geometry(gpkg)
    assert res

def test_crs(gpkg):
    res = check.check_crs(gpkg)
    assert res
