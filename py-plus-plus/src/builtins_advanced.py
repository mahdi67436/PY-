"""Advanced built-in functions for py++."""

import time
import random as py_random
import json as py_json
from datetime import datetime, timedelta
from .advanced import PyPPArray, PyPPObject, PyPPSet, AdvancedMath, StringUtils, DataValidation
from .errors import RuntimeError as PyPPRuntimeError, TypeError as PyPPTypeError

class PyPPFunction:
    """Function implementation for py++."""
    
    def __init__(self, params, body, closure):
        self.params = params
        self.body = body
        self.closure = closure
    
    def __repr__(self):
        return f"<function with {len(self.params)} params>"


# ============= Array Functions =============
def builtin_array(*items):
    """Create an array."""
    return PyPPArray(list(items))

def builtin_is_array(value):
    """Check if value is array."""
    return isinstance(value, PyPPArray)

def builtin_array_push(arr, item):
    """Push item to array."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("push() requires an array")
    arr.push(item)
    return None

def builtin_array_pop(arr):
    """Pop from array."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("pop() requires an array")
    return arr.pop()

def builtin_array_shift(arr):
    """Shift from array."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("shift() requires an array")
    return arr.shift()

def builtin_array_unshift(arr, item):
    """Unshift to array."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("unshift() requires an array")
    arr.unshift(item)
    return None

def builtin_array_reverse(arr):
    """Reverse array."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("reverse() requires an array")
    arr.reverse()
    return None

def builtin_array_sort(arr):
    """Sort array."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("sort() requires an array")
    arr.sort()
    return None

def builtin_array_slice(arr, start, end=None):
    """Slice array."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("slice() requires an array")
    if end is None:
        end = arr.length()
    return arr.slice(start, end)

def builtin_array_join(arr, separator=""):
    """Join array."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("join() requires an array")
    return arr.join(separator)

def builtin_array_includes(arr, item):
    """Check if array includes item."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("includes() requires an array")
    return arr.includes(item)

def builtin_array_indexof(arr, item):
    """Get index of item in array."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("indexOf() requires an array")
    return arr.indexOf(item)

def builtin_array_length(arr):
    """Get array length."""
    if not isinstance(arr, PyPPArray):
        raise PyPPTypeError("length() requires an array")
    return arr.length()


# ============= Object Functions =============
def builtin_object(**props):
    """Create an object."""
    return PyPPObject(props)

def builtin_is_object(value):
    """Check if value is object."""
    return isinstance(value, PyPPObject)

def builtin_object_keys(obj):
    """Get object keys."""
    if not isinstance(obj, PyPPObject):
        raise PyPPTypeError("keys() requires an object")
    return PyPPArray(obj.keys())

def builtin_object_values(obj):
    """Get object values."""
    if not isinstance(obj, PyPPObject):
        raise PyPPTypeError("values() requires an object")
    return PyPPArray(obj.values())

def builtin_object_has(obj, key):
    """Check if object has property."""
    if not isinstance(obj, PyPPObject):
        raise PyPPTypeError("has() requires an object")
    return obj.has(key)

def builtin_object_get(obj, key):
    """Get object property."""
    if not isinstance(obj, PyPPObject):
        raise PyPPTypeError("get() requires an object")
    return obj.get(key)

def builtin_object_set(obj, key, value):
    """Set object property."""
    if not isinstance(obj, PyPPObject):
        raise PyPPTypeError("set() requires an object")
    obj.set(key, value)
    return None

def builtin_object_delete(obj, key):
    """Delete object property."""
    if not isinstance(obj, PyPPObject):
        raise PyPPTypeError("delete() requires an object")
    return obj.delete(key)

def builtin_object_merge(obj1, obj2):
    """Merge two objects."""
    if not isinstance(obj1, PyPPObject) or not isinstance(obj2, PyPPObject):
        raise PyPPTypeError("merge() requires two objects")
    return obj1.merge(obj2)


# ============= Set Functions =============
def builtin_set(*items):
    """Create a set."""
    return PyPPSet(list(items))

def builtin_is_set(value):
    """Check if value is set."""
    return isinstance(value, PyPPSet)

def builtin_set_add(s, item):
    """Add to set."""
    if not isinstance(s, PyPPSet):
        raise PyPPTypeError("add() requires a set")
    s.add(item)
    return None

def builtin_set_remove(s, item):
    """Remove from set."""
    if not isinstance(s, PyPPSet):
        raise PyPPTypeError("remove() requires a set")
    return s.remove(item)

def builtin_set_has(s, item):
    """Check if set has item."""
    if not isinstance(s, PyPPSet):
        raise PyPPTypeError("has() requires a set")
    return s.has(item)

def builtin_set_size(s):
    """Get set size."""
    if not isinstance(s, PyPPSet):
        raise PyPPTypeError("size() requires a set")
    return s.size()

def builtin_set_union(s1, s2):
    """Union of sets."""
    if not isinstance(s1, PyPPSet) or not isinstance(s2, PyPPSet):
        raise PyPPTypeError("union() requires two sets")
    return s1.union(s2)

def builtin_set_intersection(s1, s2):
    """Intersection of sets."""
    if not isinstance(s1, PyPPSet) or not isinstance(s2, PyPPSet):
        raise PyPPTypeError("intersection() requires two sets")
    return s1.intersection(s2)

def builtin_set_difference(s1, s2):
    """Difference of sets."""
    if not isinstance(s1, PyPPSet) or not isinstance(s2, PyPPSet):
        raise PyPPTypeError("difference() requires two sets")
    return s1.difference(s2)


# ============= Math Functions =============
def builtin_sqrt(n):
    """Square root."""
    return AdvancedMath.sqrt(n)

def builtin_sin(n):
    """Sine."""
    return AdvancedMath.sin(n)

def builtin_cos(n):
    """Cosine."""
    return AdvancedMath.cos(n)

def builtin_tan(n):
    """Tangent."""
    return AdvancedMath.tan(n)

def builtin_log(n, base=10):
    """Logarithm."""
    return AdvancedMath.log(n, base)

def builtin_exp(n):
    """Exponential."""
    return AdvancedMath.exp(n)

def builtin_floor(n):
    """Floor."""
    return AdvancedMath.floor(n)

def builtin_ceil(n):
    """Ceiling."""
    return AdvancedMath.ceil(n)

def builtin_round(n, precision=0):
    """Round."""
    return AdvancedMath.round(n, precision)

def builtin_gcd(a, b):
    """GCD."""
    return AdvancedMath.gcd(a, b)

def builtin_lcm(a, b):
    """LCM."""
    return AdvancedMath.lcm(a, b)

def builtin_abs(n):
    """Absolute value."""
    return abs(n)

def builtin_min(*args):
    """Minimum value."""
    if not args:
        raise PyPPRuntimeError("min() requires at least one argument")
    return min(args)

def builtin_max(*args):
    """Maximum value."""
    if not args:
        raise PyPPRuntimeError("max() requires at least one argument")
    return max(args)


# ============= String Functions =============
def builtin_uppercase(s):
    """Uppercase."""
    return StringUtils.uppercase(str(s))

def builtin_lowercase(s):
    """Lowercase."""
    return StringUtils.lowercase(str(s))

def builtin_capitalize(s):
    """Capitalize."""
    return StringUtils.capitalize(str(s))

def builtin_trim(s):
    """Trim whitespace."""
    return StringUtils.trim(str(s))

def builtin_string_split(s, sep=" "):
    """Split string."""
    return StringUtils.split(str(s), sep)

def builtin_string_replace(s, find, repl):
    """Replace in string."""
    return StringUtils.replace(str(s), find, repl)

def builtin_string_substring(s, start, end=None):
    """Get substring."""
    if end is None:
        end = len(s)
    return StringUtils.substring(str(s), start, end)

def builtin_string_indexof(s, search):
    """Index of substring."""
    return StringUtils.indexOf(str(s), search)

def builtin_string_startswith(s, search):
    """Starts with."""
    return StringUtils.startsWith(str(s), search)

def builtin_string_endswith(s, search):
    """Ends with."""
    return StringUtils.endsWith(str(s), search)

def builtin_string_includes(s, search):
    """Includes substring."""
    return StringUtils.includes(str(s), search)

def builtin_string_repeat(s, count):
    """Repeat string."""
    return StringUtils.repeat(str(s), count)


# ============= Validation Functions =============
def builtin_is_number(value):
    """Check if number."""
    return DataValidation.is_number(value)

def builtin_is_string(value):
    """Check if string."""
    return DataValidation.is_string(value)

def builtin_is_boolean(value):
    """Check if boolean."""
    return DataValidation.is_boolean(value)

def builtin_is_null(value):
    """Check if null."""
    return DataValidation.is_null(value)

def builtin_is_function(value):
    """Check if function."""
    return DataValidation.is_function(value)


# ============= Misc Functions =============
def builtin_print(*args):
    """Print output."""
    print(*args)
    return None

def builtin_len(obj):
    """Get length."""
    if isinstance(obj, PyPPArray):
        return obj.length()
    if isinstance(obj, PyPPSet):
        return obj.size()
    return len(obj)

def builtin_range(*args):
    """Create range."""
    return PyPPArray(list(range(*args)))

def builtin_time():
    """Current time."""
    return time.time()

def builtin_sleep(seconds):
    """Sleep."""
    time.sleep(seconds)
    return None

def builtin_random():
    """Random number."""
    return py_random.random()

def builtin_randint(a, b):
    """Random integer."""
    return py_random.randint(a, b)

def builtin_int(value):
    """Convert to int."""
    return int(value)

def builtin_float(value):
    """Convert to float."""
    return float(value)

def builtin_str(value):
    """Convert to string."""
    return str(value)

def builtin_bool(value):
    """Convert to bool."""
    return bool(value)

def builtin_type(obj):
    """Get type name."""
    if isinstance(obj, PyPPArray):
        return "array"
    if isinstance(obj, PyPPObject):
        return "object"
    if isinstance(obj, PyPPSet):
        return "set"
    if isinstance(obj, PyPPFunction):
        return "function"
    return type(obj).__name__

def builtin_typeof(obj):
    """Typeof operator."""
    return builtin_type(obj)

def builtin_json_stringify(obj):
    """Convert to JSON string."""
    def to_serializable(obj):
        if isinstance(obj, PyPPArray):
            return [to_serializable(item) for item in obj.items]
        if isinstance(obj, PyPPObject):
            return {k: to_serializable(v) for k, v in obj.properties.items()}
        if isinstance(obj, PyPPSet):
            return list(obj.items)
        return obj
    
    return py_json.dumps(to_serializable(obj))

def builtin_json_parse(json_str):
    """Parse JSON string."""
    def from_json(obj):
        if isinstance(obj, dict):
            return PyPPObject(obj)
        if isinstance(obj, list):
            return PyPPArray(obj)
        return obj
    
    parsed = py_json.loads(json_str)
    return from_json(parsed)


# ============= Register all builtins =============
BUILTINS = {
    # Array functions
    'array': builtin_array,
    'isArray': builtin_is_array,
    'push': builtin_array_push,
    'pop': builtin_array_pop,
    'shift': builtin_array_shift,
    'unshift': builtin_array_unshift,
    'reverse': builtin_array_reverse,
    'sort': builtin_array_sort,
    'slice': builtin_array_slice,
    'join': builtin_array_join,
    'includes': builtin_array_includes,
    'indexOf': builtin_array_indexof,
    'length': builtin_array_length,
    
    # Object functions
    'object': builtin_object,
    'isObject': builtin_is_object,
    'keys': builtin_object_keys,
    'values': builtin_object_values,
    'has': builtin_object_has,
    'get': builtin_object_get,
    'set': builtin_object_set,
    'delete': builtin_object_delete,
    'merge': builtin_object_merge,
    
    # Set functions
    'set': builtin_set,
    'isSet': builtin_is_set,
    'add': builtin_set_add,
    'remove': builtin_set_remove,
    'size': builtin_set_size,
    'union': builtin_set_union,
    'intersection': builtin_set_intersection,
    'difference': builtin_set_difference,
    
    # Math functions
    'sqrt': builtin_sqrt,
    'sin': builtin_sin,
    'cos': builtin_cos,
    'tan': builtin_tan,
    'log': builtin_log,
    'exp': builtin_exp,
    'floor': builtin_floor,
    'ceil': builtin_ceil,
    'round': builtin_round,
    'gcd': builtin_gcd,
    'lcm': builtin_lcm,
    'abs': builtin_abs,
    'min': builtin_min,
    'max': builtin_max,
    
    # String functions
    'uppercase': builtin_uppercase,
    'lowercase': builtin_lowercase,
    'capitalize': builtin_capitalize,
    'trim': builtin_trim,
    'split': builtin_string_split,
    'replace': builtin_string_replace,
    'substring': builtin_string_substring,
    'startsWith': builtin_string_startswith,
    'endsWith': builtin_string_endswith,
    'repeat': builtin_string_repeat,
    
    # Validation functions
    'isNumber': builtin_is_number,
    'isString': builtin_is_string,
    'isBoolean': builtin_is_boolean,
    'isNull': builtin_is_null,
    'isFunction': builtin_is_function,
    
    # Misc functions
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
    'typeof': builtin_typeof,
    'stringify': builtin_json_stringify,
    'parse': builtin_json_parse,
}
