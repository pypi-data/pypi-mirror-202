import re
import os
import inspect
import argparse
import ctypes
import sys

global var_list
var_list = {}

def parse_value(value):
    if value.isdigit():
        return int(value)
    elif "." in value and value.replace(".", "", 1).isdigit():
        return float(value)
    elif value.lower() == "none":
        return None
    elif value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    elif value == "":
        return None
    else:
        return value.strip("'\"")


def parse_string(s):
    d = {}
    items = re.findall(r'([^=,]+(?:\[[^\]]*\])?)=?(\[[^\]]*\]|[^,]*)', s)
    for key, value in items:
        if value.startswith("[") and value.endswith("]"):
            value = value[1:-1].split(",")
            value = [parse_value(v) for v in value]
        else:
            value = parse_value(value)
        d[key] = value
    return d

#s = "a=1,b,c=[1,2,3],d=4,e=3.2,f=itud,g=False"
def parse_env(name):
    env_vars = os.environ
    value = env_vars[name]
    result = parse_string(value)
    var_list[name] = result
    var_list[name + "_str"] = value

"""for key, value in env_vars.items():
    result = parse_string(value)
    if key not in globals():
        globals()[key] = result
        globals()[key + "_str"] = value"""


def get_hyper(name):
    if name not in var_list:
        if name in os.environ:
            parse_env(name)
        elif f"--{name}" in sys.argv:
            parse_arg(name)
        else:
            return {}
    return var_list[name]

def get_hyper_str(name):
    if name not in var_list:
        get_hyper(name)
    return var_list[name + "_str"]

def parse_arg(name):
    parser = argparse.ArgumentParser()
    parser.add_argument(f"--{name}", type=str, default="")
    args, unknown_args = parser.parse_known_args()
    value = getattr(args, name)
    result = parse_string(value)
    var_list[name] = result
    var_list[name + "_str"] = value
    sys.argv = [sys.argv[0]] + unknown_args

def reset_hyper(hyper, pargs=None):
    if type(hyper) is str:
        hyper = get_hyper(hyper)
    if pargs is None:
        frame = inspect.currentframe().f_back
        pargs = frame.f_locals
    for k in hyper:
        v = hyper[k]
        if isinstance(pargs, argparse.Namespace) and hasattr(pargs, k):
            setattr(pargs, k, v)
        elif k in pargs:
            pargs[k] = v
    if 'frame' in locals():
        ctypes.pythonapi.PyFrame_LocalsToFast(ctypes.py_object(frame), ctypes.c_int(0))
    

