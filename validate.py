import os
import sys

_here = os.path.abspath(__file__)
sys.path.insert(0, _here)


config = {
    'geo_path': 'tmp/PM-MAR-MS-Arsinoes_01/vector/PM-MAR-MS-Arsinoes_01.gpkg',
    'geopackage_tables': ['units', 'contacts']
}

from validator import Validator

def run(config, log_path):
    validator = Validator(config, log_path)
    res = validator.run()
    return res


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--log', default=None, type=str)
    parser.add_argument('--cfg', default=None, type=str)

    args = parser.parse_args()
    # res = run(args.cfg, args.log)
    res = run(config, 'log.log')
