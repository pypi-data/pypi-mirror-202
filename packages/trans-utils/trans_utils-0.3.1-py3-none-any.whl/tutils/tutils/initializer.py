"""
    usage:
        args = trans_args()
        logger, config = trans_init(args)
    or:
        args = trans_args(parser)
        logger, config = trans_init(args, ex_config=BASE_CONFIG)
    

"""
# from termcolor import colored
import yaml
import yamlloader
# from pathlib import Path
import argparse
import sys
from collections import OrderedDict
from datetime import datetime
import os

from .tlogger import MultiLogger
from .tutils import dump_yaml, save_script
import copy
from .functools import _clear_config, _print_dict, tprint
from .tutils import save_script
from typing import Any, Dict, List
from .tutils import tfilename,_get_time_str

import shutil



BASE_CONFIG = {
    # params used in Initializer
    'base': {
        'base_dir': './runs_debug/',
        'experiment': "",
        'tag': '',
        'stage': '', 
        'extag': '',
        'config': '',
        'test': False,
        'func': 'train',
        'gpus': '',
        'ms': False,
        'runs_dir': None, # 
        },    
    # params used in Logger
    'logger':{
        'use_logger': True,
        'record_mode': ["tensorboard"], # "wandb", "tensorboard", 'csv'
        'action': 'k', 
        'logging_mode': None,
    },
    'training': {
        'gpus': None,
        'ddp': {
            'master_addr': 'localhost',
            'master_port': '25807',
            },
        'num_epochs' : 2500, 
        'batch_size' : 8,
        'num_workers' : 8,
        'save_interval' : 50,
        'load_pretrain_model': False,
        'load_optimizer': False,
        'val_check_interval': 10,
        'use_amp': False,
        'training_log_interval': 1,
        'save_latest_only': False,
        'save_all_records': True,
    },
}

class TConfig:
    def __init__(self, file, mode:str, parser, ex_config=None, clear_none=True, saving_script=True, **kwargs) -> None:
        self.file = file
        self.default_parser = parser
        if mode.lower() in ['sc', 'script']:            self.mode = "sc"
        elif mode.lower() in ['nb', 'notebook']:            self.mode = "nb"
        elif mode.lower() in ['ddp', 'dp']:            self.mode = "ddp"
        else:            raise ValueError(f"TypeError, Got {mode}")
        self.logger = None
        self.args = None
        self.config = self._set_config(parser=parser, ex_config=ex_config, file=file, clear_none=clear_none, saving_script=saving_script)

    def _set_config(self, parser=None, ex_config=None, file=None, clear_none=True, saving_script=True, **kwargs):
        # Load configs in args
        if self.mode == "sc":
            args = trans_args(parser)
            self.args = args
            assert args is not None
        else: args = None

        # Load configs in config.yaml
        file_config = None
        if args is not None: 
            if args.config is not None:
                with open(args.config) as f:
                    file_config = yaml.load(f, Loader=yamlloader.ordereddict.CLoader)

        # Merge configs
        config = merge_configs(args=args, file_config=file_config, ex_config=ex_config, clear_none=clear_none)
        
        # Setup path of runs_dir
        if self.file is not None or file is not None:
            parent, name = os.path.split(self.file)
            name = name[:-3]
            print(f"Change experiment name from {config['base']['experiment']} to {name}")
            config['base']['experiment'] = name
        config = _check_config(config)
        config['base']['__INFO__']['Argv'] = "Argv: python " + ' '.join(sys.argv)

        # Save scripts
        if saving_script and file is not None:
            print(f"Save running script to {config['base']['runs_dir']} from {file}")
            save_script(config['base']['runs_dir'], file)
        
        self.config = config
        return config

    def get_logger(self, **kwargs):
        if self.config is None:
            raise ValueError("Please call 'TConfig.get_config(...)' first! ")
        config = self.config
        logger = get_logger(config)
        config['base']['__INFO__']['logger'] = logger.record_mode
        dump_yaml(logger, _clear_config(config), path=config['base']['runs_dir'] + "/configs/config.yaml")
        self.logger = logger
        return logger

    def get_args(self, parser=None):
        if self.args is None:
            raise ValueError
        return self.args
    
    def get_config(self):
        return self.config
    

def get_logger(config):
    config_base = config['base']
    config_logger = config['logger']
    logger = MultiLogger(logdir=config_base['runs_dir'], 
                        record_mode=config_logger.get('record_mode', None), 
                        tag=config_base['tag'], 
                        extag=config_base.get('experiment', None),
                        action=config_logger.get('action', 'k')) # backup config.yaml
    return logger

def trans_args(parser=None, **kwargs):
    if parser is None:
        parser = argparse.ArgumentParser(description='')
    try:
        parser.add_argument("--base_dir", type=str, default="")
    except:
        print("Already add '--base_dir' ")
    try:
        parser.add_argument("-c", "--config", type=str, default='./configs/config.yaml') 
    except:
        print("Already add '--config' ")
    try:
            parser.add_argument("-t", "--tag", type=str, default="")
    except:
        print("Already add '--tag' ")
    try:
        parser.add_argument("-et", "--extag", type=str, default="")
    except:
        print("Already add '--extag' ")
    try: 
        parser.add_argument("-exp", "--experiment", type=str, default='', help="experiment name")
    except:
        print("Already add '--experiment' ")
    try:
        parser.add_argument("-st", "--stage", type=str, default="", help="stage name for multi-stage experiment ")
    except:
        print("Already add '--stage' ")
    try:
        parser.add_argument("--test", action="store_true")
    except:
        print("Already add '--test' ")
    try:
        parser.add_argument("--func", type=str, default="train", help=" function name for test specific funciton ")
    except:
        print("Already add '--func' ")
    try:
        parser.add_argument("--ms", action="store_true", help=" Turn on Multi stage mode ! ")
    except:
        print("Already add '--ms' ")
    try:
        parser.add_argument("--gpus", type=str, default='', help=" Turn on Multi stage mode ! ")
    except:
        print("Already add '--gpus' ")
    args = parser.parse_args()
    return args   


def _check_config(config):    
    config_base = config['base']
    config['base']['tag'] = config['base']['tag'] if ('tag' in config['base'].keys()) and (config['base']['tag']!="") else str(datetime.now()).replace(' ', '-')
    config['base']['extag'] = config['base']['extag'] if 'extag' in config['base'].keys() else None
    config['base']['__INFO__'] = {}
    config['base']['__INFO__']['runtime'] = str(datetime.now()).replace(' ', '-')

    experiment = config['base']['experiment'] if 'experiment' in config['base'].keys() else ''
    stage = config['base']['stage'] if 'stage' in config['base'].keys() else ''

    config['base']['runs_dir'] = os.path.join(config['base']['base_dir'], experiment, config['base']['tag'], stage)
    if not os.path.exists(config['base']['runs_dir']):
        print(f"Make dir '{config['base']['runs_dir']}' !")
        os.makedirs(config['base']['runs_dir'])
    return config


def merge_configs(args=None, file_config=None, ex_config=None, clear_none=True):
    assert isinstance(ex_config, (dict, type(None))), f"Got ex_config: {ex_config}"

    # Load yaml config file
    config=BASE_CONFIG
    #  --------  file_config < args < ex_config  ----------
    file_config = file_config if file_config is not None else {}
    ex_config = ex_config if ex_config is not None else {}
    # Clear some vars with None or ""
    arg_dict_special = vars(copy.deepcopy(args)) if args is not None else {}

    if clear_none:
        file_config = _clear_config(file_config)
        arg_dict_special = _clear_config(arg_dict_special)
        ex_config   = _clear_config(ex_config)

    # Merge file_config to base_config
    config = merge_cascade_dict([config, file_config])

    # merge arg_config to config
    for k, v in config['base'].items():
        if k in arg_dict_special.keys():
            config['base'][k] = arg_dict_special.pop(k)
    arg_dict = {'special': arg_dict_special}
    print("debug: arg-dict")
    _print_dict(arg_dict)

    # Merge ex-config to config
    config = merge_cascade_dict([config, arg_dict, ex_config])
    return config


def merge_cascade_dict(dicts):
    num_dict = len(dicts)
    ret_dict = {}
    for d in dicts:
        assert isinstance(d, dict), f"Got d1: {d}"
        ret_dict = _merge_two_dict(ret_dict, d)
        # print("debug: ")
        # _print_dict(ret_dict['base'])
    return ret_dict

def _merge_two_dict(d1, d2):
    # Use d2 to overlap d1
    d1 = {} if d1 is None else d1
    d2 = {} if d2 is None else d2
    assert isinstance(d1, dict), f"Got d1: {d1}"
    assert isinstance(d2, dict), f"Got d1: {d2}"
    ret_dict = {**d2, **d1}
    if isinstance(d2, dict):
        for key, value in d2.items():
            if isinstance(value, dict):
                ret_dict[key] = _merge_two_dict(ret_dict[key], d2[key])
            else:
                ret_dict[key] = d2[key]
    return ret_dict 


def dump_yaml(logger=None, config=None, path=None, verbose=True):
    # Backup existing yaml file
    assert config is not None
    path = config['base']['runs_dir'] + "/config.yaml" if path is None else path
    path = tfilename(path)
    if os.path.isfile(path):
        backup_name = path + '.' + _get_time_str()
        shutil.move(path, backup_name)
        if logger is not None:
            logger.info(f"Existing yaml file '{path}' backuped to '{backup_name}' ")
        else:
            print(f"Existing yaml file '{path}' backuped to '{backup_name}' ")
    with open(path, "w") as f:
        config = _ordereddict_to_dict(config)
        yaml.dump(config, f)
    if verbose:
        if logger is not None:
            logger.info(f"Saved config.yaml to {path}")
        else:
            print(f"Saved config.yaml to {path}")


def load_yaml(path):
    with open(path) as f:
        config = yaml.load(f, Loader=yamlloader.ordereddict.CLoader)
    return config


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