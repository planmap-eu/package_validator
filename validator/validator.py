#!/usr/bin/env python

from tasks import *

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

        tasks = [TaskVector, TaskVectorTables]
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
