#!/usr/bin/env python

from tasks import *


def check_exist(filename):
    import os
    return os.path.exists(filename)

def check_is_gpkg(filename):
    import geopandas
    try:
        geopandas.read_file(filename, driver='GPKG')
    except:
        return False
    return True

def check_layer(pkg, layer):
    out = layer in pkg
    return out

def check_gpkg_layers(filename, layers=[]):
    pkg = load_gpkg(filename)
    for layer in layers:
        out += check_layer(pkg, layer)
    return out

def check_layer_columns(gdf, columns):
    out = []
    for column in columns:
        out += column in gdf
    return out

def check_layers_columns(filename, layers={}):
    pkg = load_gpkg(filename)
    gdf = pkg[layer]
    for layer, columns in layers.items():
        out += check_layer_columns(gdf, columns)
    return out

def check_column_content(gdf, column, rules):
    for rule in rules:
        out += gdf[column].apply(rule)
    return out

def check_columns_content(filename, layer, columns={}):
    pkg = load_gpkg(filename)
    gdf = pkg[layer]
    for column, rules in columns.items():
        out += check_column_content(gdf, column, rules)
    return out

class Validator(object):
    tasks = None

    def __init__(self, config, log_path):
        """
        * 'config' is a python dict
        * 'context' is something(?) bringing global info
        """
        import logging
        logger = logging.getLogger('planmap')
        logger.setLevel('INFO')
        logger.addHandler(logging.FileHandler(log_path))
        self.log = logger

        self.config = config

        # tasks = [TaskVector, TaskVectorTables]
        tasks = [check_exist(filename),
                 check_is_gpkg(filename),
                 check_gpkg_layers(filename),
                 check_layers_columns(filename),
                 check_columns_content(filename)]
        self.tasks = self.set_tasks(tasks)

    def set_tasks(self, tasks):
        return [t(config=self.config, logger=self.log) for t in tasks]

    def run(self):
        ok = True
        for task in self.tasks:
            res = task.run()
            if not res:
                self.log.error(f'Task {task} failed')
                ok = False
                break
        return ok
