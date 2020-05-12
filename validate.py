#!/usr/bin/env python
"""
Get a package path and check its content.

The package content checking is processed by a series/pipeline of tasks
on specific request or automatically (if None asked) after parsing/interpreting
the package name, or greedly inpecting any of the expected directories.
"""
import os
import sys

# _here = os.path.abspath(__file__)
# sys.path.insert(0, _here)
#
# from validator import Validator
#
# config = {
#     'geo_path': 'tmp/PM-MAR-MS-Arsinoes_01/vector/PM-MAR-MS-Arsinoes_01.gpkg',
#     'geopackage_tables': ['units', 'contacts']
# }


from itertools import zip_longest

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

    pkg_specs = {field: lookup.get(field, lambda t:t)(token)
                            for field,token in zip_longest(fields,tokens)}
    return pkg_specs


def run(pkg_path, log_path):
    #parse package name
    pkg_name = os.path.basename(os.path.abspath(pkg_path))
    pkg_specs = parse_package_name(pkg_name)
    print(pkg_specs)
    # body,dtype,label,sublabel = pkg_specs


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--log', default=None, type=str)
    # parser.add_argument('--cfg', default=None, type=str)
    parser.add_argument('path', type=str,
                        help="Path of PlanMap package")

    args = parser.parse_args()
    pkg_path = args.path

    # res = run(args.cfg, args.log)

    res = run(pkg_path, 'validator.log')
