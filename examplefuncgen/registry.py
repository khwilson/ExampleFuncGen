import importlib
import json as _json
from pkg_resources import resource_filename as _resource

import six


def gen_function(fq_name, args):
    module_name, func_name = fq_name.split(':')
    module = importlib.import_module(module_name)
    return getattr(module, func_name)(*args)


def get_function(fq_name):
    module_name, func_name = fq_name.split(':')
    module = importlib.import_module(module_name)
    return getattr(module, func_name)


class Registry(object):

    __instance = None

    def __init__(self):
        with open(_resource('examplefuncgen', 'features_and_imputers.json'), 'r') as _the_file:
            _the_features = _json.load(_the_file)

        for feature_name, value in _the_features.items():
            if 'compute_function_gen' in value:
                args = value.get('compute_function_gen_args', ())
                computer = gen_function(value['compute_function_gen'], args)
            else:
                computer = get_function(value['compute_function'])

            if 'impute_function_gen' in value:
                args = value.get('impute_function_gen_args', ())
                imputer = gen_function(value['impute_function_gen'], args)
            else:
                imputer = get_function(value['impute_function'])

            feature = type(feature_name, (), {'compute': staticmethod(computer),
                                              'impute': staticmethod(imputer)})

            setattr(self, feature_name, feature)

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = Registry()
        return cls.__instance
