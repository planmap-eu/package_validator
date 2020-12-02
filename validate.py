import os
import check

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Validate Geopackages")

    parser.add_argument('gpkg', type=str,
                        help="File/path to Geopackage")

    args = parser.parse_args()

    filename = args.gpkg
    assert os.path.isfile(filename), f"Filename '{filename}' does not exist"

    check.geopackage(filename)
