"""Advanced features for py++ language."""

from typing import Any, Dict, List, Callable
from .errors import RuntimeError as PyPPRuntimeError, TypeError as PyPPTypeError

class PyPPArray:
    """Array/List implementation for py++."""
    
    def __init__(self, items: List[Any] = None):
        self.items = items or []
    
    def push(self, item: Any) -> None:
        """Add item to end of array."""
        self.items.append(item)
    
    def pop(self) -> Any:
        """Remove and return last item."""
        if not self.items:
            raise PyPPRuntimeError("Cannot pop from empty array")
        return self.items.pop()
    
    def shift(self) -> Any:
        """Remove and return first item."""
        if not self.items:
            raise PyPPRuntimeError("Cannot shift from empty array")
        return self.items.pop(0)
    
    def unshift(self, item: Any) -> None:
        """Add item to beginning of array."""
        self.items.insert(0, item)
    
    def length(self) -> int:
        """Get array length."""
        return len(self.items)
    
    def get(self, index: int) -> Any:
        """Get item at index."""
        if not isinstance(index, int):
            raise PyPPTypeError(f"Array index must be int, got {type(index).__name__}")
        if index < 0 or index >= len(self.items):
            raise PyPPRuntimeError(f"Array index out of bounds: {index}")
        return self.items[index]
    
    def set(self, index: int, value: Any) -> None:
        """Set item at index."""
        if not isinstance(index, int):
            raise PyPPTypeError(f"Array index must be int, got {type(index).__name__}")
        if index < 0 or index >= len(self.items):
            raise PyPPRuntimeError(f"Array index out of bounds: {index}")
        self.items[index] = value
    
    def reverse(self) -> None:
        """Reverse array in place."""
        self.items.reverse()
    
    def sort(self) -> None:
        """Sort array in place."""
        try:
            self.items.sort()
        except TypeError:
            raise PyPPRuntimeError("Cannot sort array with incomparable types")
    
    def slice(self, start: int, end: int) -> 'PyPPArray':
        """Get slice of array."""
        if not isinstance(start, int) or not isinstance(end, int):
            raise PyPPTypeError("Slice indices must be integers")
        return PyPPArray(self.items[start:end])
    
    def map(self, fn: Callable) -> 'PyPPArray':
        """Apply function to each element."""
        from .builtins import PyPPFunction
        if isinstance(fn, PyPPFunction):
            new_items = []
            for item in self.items:
                result = fn.call([item], {})
                new_items.append(result)
            return PyPPArray(new_items)
        raise PyPPTypeError(f"map() requires a function, got {type(fn).__name__}")
    
    def filter(self, fn: Callable) -> 'PyPPArray':
        """Filter array with function."""
        from .builtins import PyPPFunction
        if isinstance(fn, PyPPFunction):
            new_items = []
            for item in self.items:
                result = fn.call([item], {})
                if result:  # Truthy check
                    new_items.append(item)
            return PyPPArray(new_items)
        raise PyPPTypeError(f"filter() requires a function, got {type(fn).__name__}")
    
    def reduce(self, fn: Callable, initial: Any = None) -> Any:
        """Reduce array with function."""
        from .builtins import PyPPFunction
        if isinstance(fn, PyPPFunction):
            if not self.items and initial is None:
                raise PyPPRuntimeError("Reduce of empty array with no initial value")
            
            start_idx = 0
            if initial is None:
                accumulator = self.items[0]
                start_idx = 1
            else:
                accumulator = initial
            
            for i in range(start_idx, len(self.items)):
                accumulator = fn.call([accumulator, self.items[i]], {})
            return accumulator
        raise PyPPTypeError(f"reduce() requires a function, got {type(fn).__name__}")
    
    def join(self, separator: str = "") -> str:
        """Join array items with separator."""
        return separator.join(str(item) for item in self.items)
    
    def includes(self, item: Any) -> bool:
        """Check if array includes item."""
        return item in self.items
    
    def indexOf(self, item: Any) -> int:
        """Find index of item."""
        try:
            return self.items.index(item)
        except ValueError:
            return -1
    
    def __str__(self) -> str:
        return f"[{', '.join(str(item) for item in self.items)}]"
    
    def __repr__(self) -> str:
        return self.__str__()


class PyPPObject:
    """Object/Dictionary implementation for py++."""
    
    def __init__(self, properties: Dict[str, Any] = None):
        self.properties = properties or {}
    
    def get(self, key: str) -> Any:
        """Get property value."""
        if key not in self.properties:
            raise PyPPRuntimeError(f"Property '{key}' not found on object")
        return self.properties[key]
    
    def set(self, key: str, value: Any) -> None:
        """Set property value."""
        self.properties[key] = value
    
    def has(self, key: str) -> bool:
        """Check if property exists."""
        return key in self.properties
    
    def keys(self) -> List[str]:
        """Get all property names."""
        return list(self.properties.keys())
    
    def values(self) -> List[Any]:
        """Get all property values."""
        return list(self.properties.values())
    
    def delete(self, key: str) -> bool:
        """Delete property."""
        if key in self.properties:
            del self.properties[key]
            return True
        return False
    
    def merge(self, other: 'PyPPObject') -> 'PyPPObject':
        """Merge two objects."""
        if not isinstance(other, PyPPObject):
            raise PyPPTypeError(f"Cannot merge with {type(other).__name__}")
        new_props = {**self.properties, **other.properties}
        return PyPPObject(new_props)
    
    def __str__(self) -> str:
        items = [f"{k}: {v}" for k, v in self.properties.items()]
        return f"{{{', '.join(items)}}}"
    
    def __repr__(self) -> str:
        return self.__str__()


class PyPPSet:
    """Set implementation for py++."""
    
    def __init__(self, items: List[Any] = None):
        self.items = set()
        if items:
            for item in items:
                if isinstance(item, (list, dict)):
                    raise PyPPTypeError("Sets can only contain hashable types")
                self.items.add(item)
    
    def add(self, item: Any) -> None:
        """Add item to set."""
        if isinstance(item, (list, dict)):
            raise PyPPTypeError("Sets can only contain hashable types")
        self.items.add(item)
    
    def remove(self, item: Any) -> bool:
        """Remove item from set."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def has(self, item: Any) -> bool:
        """Check if set contains item."""
        return item in self.items
    
    def size(self) -> int:
        """Get set size."""
        return len(self.items)
    
    def union(self, other: 'PyPPSet') -> 'PyPPSet':
        """Union with another set."""
        if not isinstance(other, PyPPSet):
            raise PyPPTypeError(f"Cannot union with {type(other).__name__}")
        new_set = PyPPSet()
        new_set.items = self.items | other.items
        return new_set
    
    def intersection(self, other: 'PyPPSet') -> 'PyPPSet':
        """Intersection with another set."""
        if not isinstance(other, PyPPSet):
            raise PyPPTypeError(f"Cannot intersect with {type(other).__name__}")
        new_set = PyPPSet()
        new_set.items = self.items & other.items
        return new_set
    
    def difference(self, other: 'PyPPSet') -> 'PyPPSet':
        """Difference with another set."""
        if not isinstance(other, PyPPSet):
            raise PyPPTypeError(f"Cannot diff with {type(other).__name__}")
        new_set = PyPPSet()
        new_set.items = self.items - other.items
        return new_set
    
    def __str__(self) -> str:
        return f"{{{', '.join(str(item) for item in self.items)}}}"
    
    def __repr__(self) -> str:
        return self.__str__()


class Decorator:
    """Function decorator support."""
    
    def __init__(self, func: Callable):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class AdvancedMath:
    """Advanced mathematical functions."""
    
    @staticmethod
    def sqrt(n: float) -> float:
        """Square root."""
        if n < 0:
            raise PyPPRuntimeError("Cannot compute sqrt of negative number")
        return n ** 0.5
    
    @staticmethod
    def sin(n: float) -> float:
        """Sine function."""
        import math
        return math.sin(n)
    
    @staticmethod
    def cos(n: float) -> float:
        """Cosine function."""
        import math
        return math.cos(n)
    
    @staticmethod
    def tan(n: float) -> float:
        """Tangent function."""
        import math
        return math.tan(n)
    
    @staticmethod
    def log(n: float, base: float = 10) -> float:
        """Logarithm."""
        if n <= 0:
            raise PyPPRuntimeError("Cannot compute log of non-positive number")
        import math
        return math.log(n, base)
    
    @staticmethod
    def exp(n: float) -> float:
        """Exponential function."""
        import math
        return math.exp(n)
    
    @staticmethod
    def floor(n: float) -> int:
        """Floor function."""
        import math
        return math.floor(n)
    
    @staticmethod
    def ceil(n: float) -> int:
        """Ceiling function."""
        import math
        return math.ceil(n)
    
    @staticmethod
    def round(n: float, precision: int = 0) -> float:
        """Round to precision."""
        return round(n, precision)
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Greatest common divisor."""
        import math
        return math.gcd(a, b)
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Least common multiple."""
        import math
        return abs(a * b) // math.gcd(a, b)


class StringUtils:
    """Advanced string utilities."""
    
    @staticmethod
    def uppercase(s: str) -> str:
        """Convert to uppercase."""
        return s.upper()
    
    @staticmethod
    def lowercase(s: str) -> str:
        """Convert to lowercase."""
        return s.lower()
    
    @staticmethod
    def capitalize(s: str) -> str:
        """Capitalize first letter."""
        return s.capitalize()
    
    @staticmethod
    def trim(s: str) -> str:
        """Remove leading/trailing whitespace."""
        return s.strip()
    
    @staticmethod
    def split(s: str, separator: str = " ") -> 'PyPPArray':
        """Split string into array."""
        parts = s.split(separator)
        return PyPPArray(parts)
    
    @staticmethod
    def replace(s: str, find: str, replacement: str) -> str:
        """Replace all occurrences."""
        return s.replace(find, replacement)
    
    @staticmethod
    def substring(s: str, start: int, end: int = None) -> str:
        """Get substring."""
        if end is None:
            return s[start:]
        return s[start:end]
    
    @staticmethod
    def indexOf(s: str, search: str) -> int:
        """Find index of substring."""
        try:
            return s.index(search)
        except ValueError:
            return -1
    
    @staticmethod
    def startsWith(s: str, search: str) -> bool:
        """Check if string starts with."""
        return s.startswith(search)
    
    @staticmethod
    def endsWith(s: str, search: str) -> bool:
        """Check if string ends with."""
        return s.endswith(search)
    
    @staticmethod
    def includes(s: str, search: str) -> bool:
        """Check if string includes."""
        return search in s
    
    @staticmethod
    def repeat(s: str, count: int) -> str:
        """Repeat string count times."""
        return s * count


class DataValidation:
    """Data validation utilities."""
    
    @staticmethod
    def is_number(value: Any) -> bool:
        """Check if value is a number."""
        return isinstance(value, (int, float))
    
    @staticmethod
    def is_string(value: Any) -> bool:
        """Check if value is a string."""
        return isinstance(value, str)
    
    @staticmethod
    def is_boolean(value: Any) -> bool:
        """Check if value is a boolean."""
        return isinstance(value, bool)
    
    @staticmethod
    def is_null(value: Any) -> bool:
        """Check if value is null."""
        return value is None
    
    @staticmethod
    def is_array(value: Any) -> bool:
        """Check if value is an array."""
        return isinstance(value, PyPPArray)
    
    @staticmethod
    def is_object(value: Any) -> bool:
        """Check if value is an object."""
        return isinstance(value, PyPPObject)
    
    @staticmethod
    def is_function(value: Any) -> bool:
        """Check if value is a function."""
        from .builtins import PyPPFunction
        return isinstance(value, PyPPFunction)
    
    @staticmethod
    def validate_type(value: Any, expected_type: str) -> bool:
        """Validate value matches type."""
        type_map = {
            'number': (int, float),
            'string': str,
            'boolean': bool,
            'array': PyPPArray,
            'object': PyPPObject,
        }
        
        if expected_type not in type_map:
            raise PyPPRuntimeError(f"Unknown type: {expected_type}")
        
        expected = type_map[expected_type]
        if isinstance(expected, tuple):
            return isinstance(value, expected)
        return isinstance(value, expected)
