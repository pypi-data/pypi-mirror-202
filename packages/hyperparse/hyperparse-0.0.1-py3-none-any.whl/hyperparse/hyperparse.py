import re
import os
import inspect
import argparse
import ctypes

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
env_vars = os.environ
for key, value in env_vars.items():
    result = parse_string(value)
    if key not in globals():
        globals()[key] = result

def set_hyper(hyper, pargs=None):
    if type(hyper) is str:
        hyper = globals()[hyper]
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
    

