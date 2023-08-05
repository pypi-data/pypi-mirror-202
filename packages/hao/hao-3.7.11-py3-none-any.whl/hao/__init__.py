import importlib
import pkgutil

from . import (
    asyncs,
    charsets,
    config,
    currencies,
    decorators,
    dicts,
    english,
    envs,
    exceptions,
    files,
    invoker,
    jsons,
    lists,
    logs,
    namespaces,
    nations,
    paths,
    regexes,
    singleton,
    slacks,
    stopwatch,
    strings,
    versions,
)

__version__ = '3.7.11'


def import_submodules(package, recursive=False):
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    caller = paths.who_called_me()
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        module_name = package.__name__ + '.' + name
        if caller == name:
            continue
        results[module_name] = importlib.import_module(module_name)
        __import__(module_name)
        if recursive and is_pkg:
            results.update(import_submodules(module_name))
    return results
