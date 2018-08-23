import importlib

from deepmerge import always_merger


def assemble_api(mntnr_apis, base_spec):
    api_spec = {}
    for api in mntnr_apis:
        module, version = api[0], api[1]
        spec = importlib.import_module(module + '.spec')
        api_spec = always_merger.merge(api_spec, spec.get_spec(version))
    return always_merger.merge(api_spec, base_spec)
