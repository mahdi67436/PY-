# py++ Advanced Features Guide

## Overview

py++ includes advanced data structures, array methods, object manipulation, and mathematical functions for professional development.

---

## 1. Arrays (Advanced Operations)

### Creating Arrays
```javascript
let arr = array(1, 2, 3, 4, 5);
let empty = array();
```

### Array Methods

#### Adding/Removing Elements
- `arr.push(item)` — Add to end
- `arr.pop()` — Remove & return last
- `arr.shift()` — Remove & return first
- `arr.unshift(item)` — Add to beginning

```javascript
let arr = array(1, 2, 3);
arr.push(4);        // [1, 2, 3, 4]
let last = arr.pop();    // last = 4, arr = [1, 2, 3]
let first = arr.shift(); // first = 1, arr = [2, 3]
arr.unshift(0);     // [0, 2, 3]
```

#### Searching
- `arr.includes(item)` — Check if contains
- `arr.indexOf(item)` — Find position (-1 if not found)

```javascript
let arr = array(1, 2, 3, 4, 5);
arr.includes(3);     // true
arr.includes(10);    // false
arr.indexOf(4);      // 3
arr.indexOf(10);     // -1
```

#### Transforming
- `arr.reverse()` — Reverse in place
- `arr.sort()` — Sort in place
- `arr.slice(start, end)` — Get sub-array

```javascript
let arr = array(3, 1, 4, 1, 5);
arr.reverse();       // [5, 1, 4, 1, 3]
arr.sort();          // [1, 1, 3, 4, 5]
arr.slice(1, 4);     // [1, 3, 4]
```

#### Combining
- `arr.join(sep)` — Join to string with separator
- `arr.length()` — Get array length

```javascript
let arr = array("apple", "banana", "orange");
arr.join(", ");      // "apple, banana, orange"
arr.length();        // 3
```

---

## 2. Objects (Key-Value Storage)

### Creating Objects
```javascript
let obj = object(
    name: "Mahdi",
    age: 25,
    email: "mahdi@example.com"
);
```

### Object Methods

#### Access Properties
```javascript
obj.name;            // "Mahdi"
obj.get("name");     // "Mahdi"
obj["name"];         // Not yet supported, use obj.name
```

#### Modify Properties
```javascript
obj.age = 26;        // Set existing
obj.job = "Dev";     // Add new
obj.set("city", "NYC");  // Alternative syntax
```

#### Check Properties
```javascript
obj.has("name");     // true
obj.has("email");    // false
```

#### Delete Properties
```javascript
obj.delete("age");   // true if existed
```

#### Get All Keys/Values
```javascript
obj.keys();          // ["name", "age", "email"]
obj.values();        // ["Mahdi", 25, "mahdi@example.com"]
```

#### Merge Objects
```javascript
let person = object(name: "Mahdi", age: 25);
let contact = object(email: "m@example.com", phone: "123-456");
let merged = person.merge(contact);
// merged = {name: "Mahdi", age: 25, email: "...", phone: "..."}
```

---

## 3. Sets (Unique Collections)

### Creating Sets
```javascript
let s = set(1, 2, 3, 4, 5);
let unique = set();
```

### Set Methods

#### Add/Remove
```javascript
let s = set(1, 2, 3);
s.add(4);            // {1, 2, 3, 4}
s.remove(2);         // {1, 3, 4}
```

#### Check Membership
```javascript
s.has(1);            // true
s.has(5);            // false
s.size();            // 3
```

#### Set Operations
```javascript
let s1 = set(1, 2, 3);
let s2 = set(2, 3, 4);

s1.union(s2);        // {1, 2, 3, 4}
s1.intersection(s2); // {2, 3}
s1.difference(s2);   // {1}
```

---

## 4. Advanced Math Functions

### Basic Math
```javascript
sqrt(16);            // 4
abs(-5);             // 5
min(3, 1, 4, 1, 5);  // 1
max(3, 1, 4, 1, 5);  // 5
round(3.7);          // 4
```

### Trigonometry
```javascript
sin(0);              // 0
cos(0);              // 1
tan(0);              // 0
```

### Logarithms & Exponentials
```javascript
log(100, 10);        // 2
log(8, 2);           // 3
exp(1);              // 2.718...
```

### Rounding Precision
```javascript
let pi = 3.14159;
round(pi);           // 3
round(pi, 2);        // 3.14
round(pi, 4);        // 3.1416
floor(pi);           // 3
ceil(pi);            // 4
```

### Number Theory
```javascript
gcd(12, 8);          // 4
lcm(12, 8);          // 24
gcd(100, 50);        // 50
```

---

## 5. Advanced String Functions

### Case Conversion
```javascript
let str = "Hello World";
uppercase(str);      // "HELLO WORLD"
lowercase(str);      // "hello world"
capitalize(str);     // "Hello world"
```

### Searching
```javascript
let text = "The quick brown fox";
startsWith(text, "The");      // true
endsWith(text, "fox");        // true
includes(text, "quick");      // true
indexOf(text, "brown");       // 10
```

### Manipulation
```javascript
let str = "hello";
substring(str, 0, 3);         // "hel"
substring(str, 2);            // "llo"
replace(str, "ll", "**");     // "he**o"
repeat(str, 3);               // "hellohellohello"
trim("  spaces  ");           // "spaces"
```

### Splitting
```javascript
split("a,b,c", ",");          // ["a", "b", "c"]
split("hello", "");           // ["h", "e", "l", "l", "o"]
```

---

## 6. Type Checking & Validation

### Type Predicates
```javascript
isNumber(42);        // true
isNumber("42");      // false

isString("hello");   // true
isString(42);        // false

isBoolean(true);     // true
isBoolean(1);        // false

isNull(null);        // true
isNull(0);           // false

isArray(array(1,2)); // true
isObject(object(a:1)); // true
isFunction(fn);      // true
```

### Type Names
```javascript
typeof(42);          // "int"
typeof("hello");     // "string"
typeof(true);        // "bool"
typeof(array(1));    // "array"
typeof(object(a:1)); // "object"
typeof(fn);          // "function"
```

### Type Conversion
```javascript
int("123");          // 123
int(3.14);           // 3

float("3.14");       // 3.14
float(42);           // 42.0

str(42);             // "42"
str(true);           // "true"

bool(1);             // true
bool(0);             // false
bool("");            // false
bool("hello");       // true
```

---

## 7. Complete Example: Personal Database

```javascript
// Create database of people
let people = array();

// Add person
let person1 = object(
    name: "Mahdi",
    age: 25,
    skills: array("Python", "JavaScript", "C++")
);

people.push(person1);

let person2 = object(
    name: "Sarah",
    age: 23,
    skills: array("Java", "Python", "SQL")
);

people.push(person2);

// Print all people
for person in people {
    print("Name: " + person.name);
    print("Age: " + person.age);
    print("Skills: " + person.skills.join(", "));
    print("");
}

// Find developers with Python
let python_devs = array();
for person in people {
    let skills = person.skills;
    if (skills.includes("Python")) {
        python_devs.push(person.name);
    }
}

print("Python developers: " + python_devs.join(", "));
```

---

## 8. Best Practices

### Use Objects for Structured Data
```javascript
// Good: Clear structure
let user = object(id: 1, name: "John", email: "john@example.com");

// Avoid: Loose arrays
let user_bad = array(1, "John", "john@example.com");
```

### Use Sets for Unique Items
```javascript
// Good: Guaranteed uniqueness
let unique_ids = set(1, 2, 3, 4);
unique_ids.add(2);  // Still 4 items

// Avoid: Manual deduplication
let ids = array(1, 2, 3, 4, 2, 3);
```

### Chain Array Methods
```javascript
let numbers = array(1, 2, 3, 4, 5);
numbers.sort();
numbers.reverse();
print(numbers.join(", "));  // "5, 4, 3, 2, 1"
```

### Validate Types Early
```javascript
fn process_data(data: array) {
    if (!isArray(data)) {
        print("Error: Expected array");
        return;
    }
    // Safe to use array methods
}
```

---

## 9. Performance Tips

1. **Use `set()` for membership checks** instead of `array.includes()`
2. **Use `object()` for named lookups** instead of parallel arrays
3. **Avoid unnecessary `slice()` operations** - creates new arrays
4. **Use `join()` for string concatenation** with many items
5. **Pre-allocate arrays** when size is known

---

## 10. Common Patterns

### Deduplicate Array
```javascript
let arr = array(1, 2, 2, 3, 3, 3);
let unique = set();
for item in arr {
    unique.add(item);
}
// Process unique values
```

### Group By Property
```javascript
let users = array(
    object(type: "admin", name: "Alice"),
    object(type: "user", name: "Bob"),
    object(type: "admin", name: "Charlie")
);

let by_type = object(admin: array(), user: array());
for user in users {
    let type = user.type;
    by_type.get(type).push(user.name);
}
```

### Merge Multiple Objects
```javascript
let config = object(host: "localhost", port: 8080);
let overrides = object(port: 9000);
let final = config.merge(overrides);
// final = {host: "localhost", port: 9000}
```

---

## Summary

| Feature | Use Case |
|---------|----------|
| **Arrays** | Ordered collections, lists |
| **Objects** | Key-value pairs, records |
| **Sets** | Unique items, membership tests |
| **Math Funcs** | Scientific calculations |
| **String Funcs** | Text processing |
| **Type Funcs** | Data validation |

For more help, check:
- [docs/guide.md](../docs/guide.md) - Core syntax
- [examples/](../examples/) - More examples
- [QUICKSTART.md](../QUICKSTART.md) - Quick reference
