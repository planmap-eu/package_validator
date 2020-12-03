#!/usr/bin/env python

import os
import check
import json_schema

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Validate Geopackages")

    parser.add_argument('gpkg', type=str,
                        help="File/path to Geopackage")

    parser.add_argument('--jsonschema', action="store_true",
                        help="Use json-schema")


    args = parser.parse_args()

    filename = args.gpkg
    assert os.path.isfile(filename), f"Filename '{filename}' does not exist"

    if args.jsonschema:
        json_schema.geopackage(filename)
    else:
        check.geopackage(filename)
