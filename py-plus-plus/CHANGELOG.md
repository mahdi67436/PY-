# py++ CHANGELOG - Version 0.2.0

## Major Changes - Advanced Features Release

### ✨ NEW: Advanced Data Structures

#### Arrays with Full API
- `push()`, `pop()`, `shift()`, `unshift()` - Stack/Queue operations
- `reverse()`, `sort()` - In-place transformations
- `slice()` - Sub-array extraction
- `includes()`, `indexOf()` - Searching operations
- `join()` - String concatenation with separator
- `length()` - Array size
- `map()`, `filter()`, `reduce()` - Functional programming (callbacks support planned)

#### Objects as Key-Value Storage
- Property access: `obj.property` or `obj["property"]`
- Property modification: `obj.property = value`
- Methods: `get()`, `set()`, `delete()`, `has()`
- `keys()`, `values()` - Property enumeration
- `merge()` - Object composition
- Supports nested objects and mixed types

#### Sets for Unique Collections
- `add()`, `remove()` - Membership management
- `has()` - Membership testing (O(1) lookup)
- `size()` - Set cardinality
- Set operations: `union()`, `intersection()`, `difference()`
- Automatic deduplication
- Fast membership checks vs arrays

### 🔢 Mathematical Functions Enhanced

#### Trigonometric Functions
- `sin()`, `cos()`, `tan()` - Basic trig
- Works with radians

#### Logarithmic & Exponential
- `log(n, base)` - Logarithm with custom base
- `exp()` - Exponential function (e^x)
- `sqrt()` - Square root

#### Rounding & Precision
- `round(n, precision)` - Round to N decimal places
- `floor()` - Round down
- `ceil()` - Round up
- `abs()` - Absolute value

#### Number Theory
- `gcd(a, b)` - Greatest Common Divisor
- `lcm(a, b)` - Least Common Multiple
- `min()`, `max()` - Variadic min/max

### 📝 String Functions Enhanced

#### Case Conversion
- `uppercase()` - Convert to UPPERCASE
- `lowercase()` - Convert to lowercase
- `capitalize()` - Capitalize first letter

#### Searching & Matching
- `startsWith()` - Prefix check
- `endsWith()` - Suffix check
- `includes()` - Substring search
- `indexOf()` - Find substring position
- `substring()` - Extract substring

#### Manipulation
- `split()` - Split string by separator into array
- `replace()` - Find and replace all
- `repeat()` - Repeat string N times
- `trim()` - Remove leading/trailing whitespace

### ✅ Type Checking & Validation

#### Type Predicates
- `isNumber()`, `isString()`, `isBoolean()`, `isNull()`
- `isArray()`, `isObject()`, `isSet()`
- `isFunction()` - Check if callable

#### Type Information
- `typeof()` - Get type name as string
- Returns: "int", "float", "string", "bool", "array", "object", "set", "function", "null"

#### Type Conversion
- `int()` - Convert to integer
- `float()` - Convert to float
- `str()` - Convert to string
- `bool()` - Convert to boolean
- Smart conversion with type coercion

### 📦 Built-in Functions

**Total Built-in Functions: 50+**

Available as:
- Global functions: `print()`, `len()`, `range()`, `array()`, etc.
- Methods on objects: `arr.push()`, `obj.keys()`, etc.
- Standalone functions: `sqrt()`, `uppercase()`, etc.

### 📚 New Examples

Created 5 new example programs:

1. **examples/arrays.pypp** - Array operations and methods
2. **examples/objects.pypp** - Object creation and manipulation
3. **examples/advanced_math.pypp** - Math functions showcase
4. **examples/advanced_strings.pypp** - String processing
5. **examples/type_checking.pypp** - Type system demonstration

### 📖 Documentation

#### New Documentation Files
- **docs/advanced.md** - Complete advanced features guide
  - Array operations with examples
  - Object manipulation patterns
  - Set operations and use cases
  - Mathematical functions reference
  - String processing guide
  - Type checking and validation
  - Best practices and patterns
  - Common use cases

### 🏗️ Code Architecture

#### New Modules
- **src/advanced.py** - Data structure implementations
  - PyPPArray - Full array implementation
  - PyPPObject - Key-value object storage
  - PyPPSet - Unique collection implementation
  - AdvancedMath - Math utility class
  - StringUtils - String manipulation class
  - DataValidation - Type checking utilities

- **src/builtins_advanced.py** - Enhanced built-in functions
  - 50+ registered built-in functions
  - Organized by category
  - Full implementations with error handling

#### Enhanced Modules
- **setup.py** - Updated for 0.2.0 with better metadata
- **src/__init__.py** - Exports all public APIs

### 🐛 Fixes

- Fixed setup.py file reading error
- Improved error messages for type mismatches
- Better handling of edge cases in array/set operations

### 🚀 Performance Improvements

- Direct indexing in arrays (O(1))
- Constant-time set membership checks (O(1))
- Optimized string operations
- Minimal overhead on mathematical functions

### 📋 Version Information

**Release**: 0.2.0  
**Release Date**: January 28, 2026  
**Python Version**: 3.7+  
**Status**: Stable with Advanced Features

### 🔄 Upgrade Instructions

```bash
# Install or upgrade
pip install -e .

# Verify installation
python pypp_cli.py version
```

### 🎯 Next Steps (Future Phases)

- **Phase 7**: Bytecode compiler and VM (10-50x speedup)
- **Phase 8**: Package registry and distribution
- Advanced features planned:
  - Async/await support
  - Generator functions
  - List comprehensions
  - Pattern matching
  - Module system enhancements

### 📊 Statistics

| Metric | Count |
|--------|-------|
| Core Source Files | 9 |
| Advanced Modules | 2 |
| Built-in Functions | 50+ |
| Example Programs | 10 |
| Documentation Files | 6 |
| Total Lines of Code | ~5,000 |
| Test Coverage | Growing |

### 🙏 Credits

py++ Team - Dedicated to bringing Python simplicity with advanced features.

---

## Breaking Changes

None - Fully backward compatible with 0.1.0

## Deprecations

None at this time

## Security

- No external dependencies (pure Python)
- Safe type handling throughout
- Controlled error messages

---

**For detailed information, see:**
- [docs/advanced.md](docs/advanced.md) - Advanced features guide
- [INDEX.md](INDEX.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - Quick reference
