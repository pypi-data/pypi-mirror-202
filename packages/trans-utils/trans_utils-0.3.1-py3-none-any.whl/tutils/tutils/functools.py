from pathlib import Path
from datetime import datetime
from collections import OrderedDict
from .tconfig import _C


def tprint(*args, **kwargs):
    print("[Tutils] ", end="")
    print(*args, **kwargs)


def dprint(*args, **kwargs):
    if _C.TUTILS_DEBUG:
        print("[Tutils Debug] ", end="")
        print(*args, **kwargs)


def _get_time_str():
    return datetime.now().strftime('%m%d-%H%M%S')


def _clear_config(config):
    # if type(config) is dict or type(config) is OrderedDict:
    if isinstance(config, (dict, OrderedDict)):
        pop_key_list = []
        for key, value in config.items():
            # print("debug: ", key, value)
            if value is None or value == "" or value == "None":
                # print("debug: poped", key, value)
                pop_key_list.append(key)
            elif isinstance(config, (dict, OrderedDict)):
                _clear_config(value)
            else:
                pass
        for key in pop_key_list:
            config.pop(key)
    return config


def print_dict(config):
    _print_dict(config)


def _print_dict(_dict, layer=0):
    if isinstance(_dict, (dict, OrderedDict)):
        for key, value in _dict.items():
            if isinstance(value, (dict, OrderedDict)):
                print("    "*layer, key, end=":\n")
                _print_dict(value, layer+1)
            else:
                print("    "*layer, f"{key}: {value}")
    else:
        print("    "*layer, _dict)


def flatten_dict(d, parent_name=None):
    """
    flatten dict: 
    config={
        'base':
            'experiment': 'test',
    }
        ==> 
    config={
        'base.experiment': 'test',
    }
    """
    s = parent_name + "." if parent_name is not None else ""
    if isinstance(d, dict):
        _d = dict()
        for k, v in d.items():
            if not isinstance(v, dict):
                _d = {**_d, **{s+k: v}}
            else:
                _d = {**_d, **flatten_dict(d[k], s + k)}
        return _d


def _ordereddict_to_dict(d):
    if not isinstance(d, dict):
        return d
    for k, v in d.items():
        if type(v) == OrderedDict:
            v = _ordereddict_to_dict(v)
            d[k] = dict(v)
        elif type(v) == list:
            d[k] = _ordereddict_to_dict(v)
        elif type(v) == dict:
            d[k] = _ordereddict_to_dict(v)
    return d




######################################################

def _tprint(*s, end="\n", **kargs):
    if len(s) > 0:
        for x in s:
            print(x, end="")
        print("", end=end)
    if len(kargs) > 0:
        for key, item in kargs.items():
            print(key, end=": ")
            print(item, end="")
        print("", end=end)


def p(*s, end="\n", **kargs):
    if _C.TUTILS_INFO or _C.TUTILS_DEBUG or _C.TUTILS_WARNING:
        print("[Tutils Info] ", end="")
        _tprint(*s, end="\n", **kargs)


def w(*s, end="\n", **kargs):
    if _C.TUTILS_WARNING or _C.TUTILS_DEBUG:
        print("[Tutils Warning] ", end="")
        _tprint(*s, end="\n", **kargs)


def d(*s, end="\n", **kargs):
    if _C.TUTILS_DEBUG:
        print("[Tutils Debug] ", end="")
        _tprint(*s, end="\n", **kargs)
