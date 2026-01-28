# py++ v0.2.0 Quick Reference - Advanced Features

## 📚 One-Page Cheat Sheet

### Arrays
```javascript
let arr = array(1, 2, 3, 4, 5);

// Mutating methods
arr.push(6);          arr.pop();
arr.unshift(0);       arr.shift();
arr.reverse();        arr.sort();

// Access
arr.includes(3);      arr.indexOf(4);
arr.length();         arr.join(",");
arr.slice(1, 3);
```

### Objects
```javascript
let obj = object();
obj.name = "Mahdi";   obj.age = 25;

// Methods
obj.has("name");      obj.get("name");
obj.set("city", "NYC"); obj.delete("temp");
obj.keys();           obj.values();
obj.merge(other);
```

### Sets
```javascript
let s = set(1, 2, 3);

// Operations
s.add(4);             s.remove(2);
s.has(3);             s.size();
s.union(other);       s.intersection(other);
s.difference(other);
```

### Math Functions
```javascript
sqrt(25)              sin(0), cos(0), tan(0)
log(100, 10)          exp(1)
floor(3.7)            ceil(3.2)
round(3.14159, 2)     abs(-5)
gcd(12, 8)            lcm(12, 8)
min(1, 2, 3)          max(1, 2, 3)
```

### String Functions
```javascript
uppercase("hello")         lowercase("HELLO")
capitalize("hello")        trim("  text  ")
split("a,b,c", ",")       replace("old", "new")
substring(str, 0, 5)      repeat("ha", 3)
indexOf(str, "find")      includes(str, "text")
startsWith(str, "pre")    endsWith(str, "fix")
```

### Type Functions
```javascript
typeof(42)            // "int"
typeof("hello")       // "string"
typeof(true)          // "bool"
typeof(array(1))      // "array"
typeof(object())      // "object"
typeof(set(1))        // "set"

isNumber(42)          isString("x")
isBoolean(true)       isNull(null)
isArray(arr)          isObject(obj)
isFunction(fn)
```

---

## 🚀 Quick Examples

### Process Array
```javascript
let numbers = array(5, 2, 8, 1, 9);
numbers.sort();              // [1, 2, 5, 8, 9]
numbers.reverse();           // [9, 8, 5, 2, 1]
print(numbers.join(", "));   // 9, 8, 5, 2, 1
```

### Build Object
```javascript
let person = object();
person.name = "Mahdi";
person.age = 25;
print(person.keys());        // name, age
```

### Math Calculation
```javascript
print(gcd(12, 8));           // 4
print(lcm(12, 8));           // 24
print(round(3.14159, 2));    // 3.14
```

### Process String
```javascript
let text = "Hello World";
print(uppercase(text));           // HELLO WORLD
print(split(text, " "));          // Hello, World
print(replace(text, "World", "Python"));  // Hello Python
```

### Type Check
```javascript
let val = 42;
if (isNumber(val)) {
    print("It's a number!");
}
```

---

## 📊 Function Count by Category

| Category | Count | Examples |
|----------|-------|----------|
| Array | 13 | push, pop, sort, join |
| Object | 8 | keys, values, merge |
| Set | 7 | add, union, intersection |
| Math | 14 | sqrt, sin, gcd, round |
| String | 11 | uppercase, split, trim |
| Type | 11 | typeof, isNumber, etc. |
| Utility | 9 | print, len, range, etc. |
| **TOTAL** | **73** | **73 functions** |

---

## ✅ What You Can Do

✅ Store data in arrays, objects, sets  
✅ Perform mathematical calculations  
✅ Process and manipulate strings  
✅ Check and convert types  
✅ Print organized output  
✅ Work with ranges and random numbers  
✅ Build professional applications  

---

## 📖 Full Docs

- **Complete Guide**: [docs/advanced.md](docs/advanced.md)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **All Functions**: [docs/api.md](docs/api.md)
- **Examples**: [examples/](examples/) folder

---

## 🎯 Most Used Functions

```javascript
// Arrays
array(), push(), pop(), sort(), reverse(), join(), includes()

// Strings  
uppercase(), lowercase(), split(), replace(), trim()

// Type
typeof(), isNumber(), isString(), isArray(), isObject()

// Math
sqrt(), gcd(), lcm(), min(), max(), round()

// Objects
object(), keys(), values(), has(), merge()
```

---

**Start coding:** `python run.py myprogram.pypp`  
**Learn more:** Read [INDEX.md](INDEX.md)  
**See examples:** Check [examples/](examples/) folder
