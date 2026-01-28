"""Built-in functions for py++."""

import time
import random as py_random

class PyPPFunction:
    def __init__(self, params, body, closure):
        self.params = params
        self.body = body
        self.closure = closure
    
    def __repr__(self):
        return f"<function with {len(self.params)} params>"

def builtin_print(*args):
    print(*args)
    return None

def builtin_len(obj):
    return len(obj)

def builtin_range(*args):
    return list(range(*args))

def builtin_time():
    return time.time()

def builtin_sleep(seconds):
    time.sleep(seconds)
    return None

def builtin_random():
    return py_random.random()

def builtin_randint(a, b):
    return py_random.randint(a, b)

def builtin_int(value):
    return int(value)

def builtin_float(value):
    return float(value)

def builtin_str(value):
    return str(value)

def builtin_bool(value):
    return bool(value)

def builtin_type(obj):
    return type(obj).__name__

BUILTINS = {
    'print': builtin_print,
    'len': builtin_len,
    'range': builtin_range,
    'time': builtin_time,
    'sleep': builtin_sleep,
    'random': builtin_random,
    'randint': builtin_randint,
    'int': builtin_int,
    'float': builtin_float,
    'str': builtin_str,
    'bool': builtin_bool,
    'type': builtin_type,
}
