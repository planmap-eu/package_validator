import os


class TaskBase(object):
    def __init__(self, **kwargs):
        print('####################################')
        print(self.__class__.__name__)
        print(kwargs)
        print('####################################')
        self.config = kwargs['config']
        self.logger = kwargs['logger']

    def run(self):
        raise NotImplementedError


class TaskVector(TaskBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self):
        geo_path = self.config['geo_path']
        res = os.path.exists(geo_path)
        self.logger.info('File exist? {}'.format('yes' if res else 'no'))
        return res


class TaskVectorTables(TaskVector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self):
        import fiona
        geo_path = self.config['geo_path']
        layers = fiona.listlayers(geo_path)
        layers_in_config = self.config['geopackage_tables']
        res = all([layer in layers_in_config for layer in layers])
        self.logger.info(f'Do we have the layers? {res!r}')
        return res

# class TaskVectorTableColumns(TaskBase):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#
# class TaskVectorTableColumnsUnits(TaskBase):
#     table = 'units'
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
