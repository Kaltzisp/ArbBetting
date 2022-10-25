from os import path
from glob import glob
from importlib import import_module


def load_modules():
    site_paths = glob(path.join(path.dirname(__file__), "..", "website", "*.py"))
    site_list = [path.basename(site_path)[0:-3] for site_path in site_paths]
    modules = [getattr(import_module("website." + module), module) for module in site_list]
    return modules
