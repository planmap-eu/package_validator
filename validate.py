#!/usr/bin/env python
"""
Get a package path and check its content.

The package content checking is processed by a series/pipeline of tasks
on specific request or automatically (if None asked) after parsing/interpreting
the package name, or greedly inpecting any of the expected directories.
"""
import os
import sys
from itertools import zip_longest


import check

import logging

logger = logging.getLogger('planmap')
logger.setLevel('DEBUG')
if True:
    logger.addHandler(logging.StreamHandler())
else:
    LOGPATH='validator.log'
    logger.addHandler(logging.FileHandler(LOGPATH))

def parse_package_name(pkgname):
    tokens = pkgname.split('-')

    # Define the structure and parsing functions
    #
    fields = ',body,dtype,label,sublabel'.split(',')
    pm_id = {f:i for i,f in enumerate(fields)}
    targets = {'MER':'Mercury','MAR':'Mars','MOO':'Moon'}
    types = dict(S = 'Stratigraphic',
                 C = 'Compositional',
                 M = 'Morphologic',
                 D = 'Digital outcrop, geologic model/mesh',
                 G = 'Geo-structural',
                 I = 'Integrated')
    lookup = dict(
        body = lambda t:targets[t],
        dtype = lambda t:','.join(types[_] for _ in t)
    )

    print(list(zip_longest(fields,tokens)))
    pkg_specs = {field: lookup.get(field, lambda t:t)(token)
                            for field,token in zip_longest(fields,tokens)}
    return pkg_specs


def check_vector(pkg_specs, pkg_path):
    """
    Check:
    - "pkg_path/vector/pkg_name.gpkg" exist?
    - has "geologic_units,geologic_contacts,surface_features,linear_features" ?
    - do tables have mandatory columns?
    - is 'geometry' column full?
    - are all layers at the same projection?
    """
    gpkg = os.path.join(pkg_path, 'vector', pkg_specs['name']+'.gpkg')
    out = check.geopackage(gpkg)

def check_raster(pkg_specs, pkg_path):
    pass

def check_model(pkg_specs, pkg_path):
    pass

def run(geopackage):
    from validator import vector
    # Check geopackage
    out = vector.check(geopackage)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('fname', type=str,
                        help="Path of GeoPackage")
    parser.add_argument('--vector', default=False, action='store_true',
                        help="Verifies a vector data file (GeoPackage)")
    parser.add_argument('--schema', type=str,
                        help="File with metadata structure to use as model")

    args = parser.parse_args()
    if not args.vector:
        print("Implemented for vectors only")
        sys.exit(1)

    fname = args.fname
    schema = args.schema

    res = run(fname)
