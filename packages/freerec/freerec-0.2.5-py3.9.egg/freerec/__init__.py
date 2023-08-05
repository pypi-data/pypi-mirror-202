__version__ = '0.2.5'

from . import data, models, criterions, launcher, metrics, utils
from freerec.dict2obj import Config


def decalre(*, version: str):
    """
    This function checks whether the provided version matches the current version of FreeRec package. 
    If they do not match, a warning message would be printed.
    """
    if version != __version__:
        print(f"\033[1;31m [Warning] FreeRec version of {version} is required but current version is {__version__} \033[0m")


import pkg_resources
import importlib

for entry_point in pkg_resources.iter_entry_points('freerec.commands'):
    module_name, _, function_name = entry_point.value.partition(':')
    module = importlib.import_module(module_name)
    globals()[entry_point.name] = getattr(module, function_name)