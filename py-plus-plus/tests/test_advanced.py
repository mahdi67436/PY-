"""Tests for advanced features."""

import unittest
import sys
sys.path.insert(0, 'src')

from advanced import PyPPArray, PyPPObject, PyPPSet, AdvancedMath, StringUtils
from errors import RuntimeError as PyPPRuntimeError


class TestPyPPArray(unittest.TestCase):
    """Test array operations."""
    
    def test_create_array(self):
        arr = PyPPArray([1, 2, 3])
        self.assertEqual(arr.length(), 3)
    
    def test_push_pop(self):
        arr = PyPPArray([1, 2, 3])
        arr.push(4)
        self.assertEqual(arr.length(), 4)
        val = arr.pop()
        self.assertEqual(val, 4)
    
    def test_shift_unshift(self):
        arr = PyPPArray([2, 3, 4])
        arr.unshift(1)
        self.assertEqual(arr.get(0), 1)
        val = arr.shift()
        self.assertEqual(val, 1)
    
    def test_reverse(self):
        arr = PyPPArray([1, 2, 3, 4])
        arr.reverse()
        self.assertEqual(arr.get(0), 4)
        self.assertEqual(arr.get(3), 1)
    
    def test_sort(self):
        arr = PyPPArray([3, 1, 4, 1, 5])
        arr.sort()
        self.assertEqual(arr.get(0), 1)
        self.assertEqual(arr.get(4), 5)
    
    def test_includes(self):
        arr = PyPPArray([1, 2, 3, 4, 5])
        self.assertTrue(arr.includes(3))
        self.assertFalse(arr.includes(10))
    
    def test_indexof(self):
        arr = PyPPArray([1, 2, 3, 4, 5])
        self.assertEqual(arr.indexOf(3), 2)
        self.assertEqual(arr.indexOf(10), -1)
    
    def test_slice(self):
        arr = PyPPArray([1, 2, 3, 4, 5])
        sliced = arr.slice(1, 4)
        self.assertEqual(sliced.length(), 3)
        self.assertEqual(sliced.get(0), 2)
    
    def test_join(self):
        arr = PyPPArray(["a", "b", "c"])
        result = arr.join(",")
        self.assertEqual(result, "a,b,c")


class TestPyPPObject(unittest.TestCase):
    """Test object operations."""
    
    def test_create_object(self):
        obj = PyPPObject({"name": "John", "age": 30})
        self.assertEqual(obj.get("name"), "John")
        self.assertEqual(obj.get("age"), 30)
    
    def test_set_property(self):
        obj = PyPPObject()
        obj.set("name", "John")
        self.assertEqual(obj.get("name"), "John")
    
    def test_has_property(self):
        obj = PyPPObject({"name": "John"})
        self.assertTrue(obj.has("name"))
        self.assertFalse(obj.has("age"))
    
    def test_delete_property(self):
        obj = PyPPObject({"name": "John", "age": 30})
        result = obj.delete("name")
        self.assertTrue(result)
        self.assertFalse(obj.has("name"))
    
    def test_keys_values(self):
        obj = PyPPObject({"a": 1, "b": 2})
        keys = obj.keys()
        values = obj.values()
        self.assertEqual(len(keys), 2)
        self.assertEqual(len(values), 2)
    
    def test_merge(self):
        obj1 = PyPPObject({"a": 1, "b": 2})
        obj2 = PyPPObject({"b": 3, "c": 4})
        merged = obj1.merge(obj2)
        self.assertEqual(merged.get("a"), 1)
        self.assertEqual(merged.get("b"), 3)  # obj2 overrides
        self.assertEqual(merged.get("c"), 4)


class TestPyPPSet(unittest.TestCase):
    """Test set operations."""
    
    def test_create_set(self):
        s = PyPPSet([1, 2, 3])
        self.assertEqual(s.size(), 3)
    
    def test_add_remove(self):
        s = PyPPSet()
        s.add(1)
        s.add(2)
        self.assertEqual(s.size(), 2)
        removed = s.remove(1)
        self.assertTrue(removed)
        self.assertEqual(s.size(), 1)
    
    def test_has(self):
        s = PyPPSet([1, 2, 3])
        self.assertTrue(s.has(2))
        self.assertFalse(s.has(5))
    
    def test_uniqueness(self):
        s = PyPPSet([1, 2, 2, 3, 3, 3])
        self.assertEqual(s.size(), 3)
    
    def test_union(self):
        s1 = PyPPSet([1, 2, 3])
        s2 = PyPPSet([2, 3, 4])
        union = s1.union(s2)
        self.assertEqual(union.size(), 4)
        self.assertTrue(union.has(1))
        self.assertTrue(union.has(4))
    
    def test_intersection(self):
        s1 = PyPPSet([1, 2, 3])
        s2 = PyPPSet([2, 3, 4])
        inter = s1.intersection(s2)
        self.assertEqual(inter.size(), 2)
        self.assertTrue(inter.has(2))
        self.assertTrue(inter.has(3))
    
    def test_difference(self):
        s1 = PyPPSet([1, 2, 3])
        s2 = PyPPSet([2, 3, 4])
        diff = s1.difference(s2)
        self.assertEqual(diff.size(), 1)
        self.assertTrue(diff.has(1))


class TestAdvancedMath(unittest.TestCase):
    """Test math functions."""
    
    def test_sqrt(self):
        self.assertEqual(AdvancedMath.sqrt(4), 2)
        self.assertEqual(AdvancedMath.sqrt(16), 4)
    
    def test_rounding(self):
        pi = 3.14159
        self.assertEqual(AdvancedMath.round(pi), 3)
        self.assertEqual(AdvancedMath.round(pi, 2), 3.14)
        self.assertEqual(AdvancedMath.floor(pi), 3)
        self.assertEqual(AdvancedMath.ceil(pi), 4)
    
    def test_gcd(self):
        self.assertEqual(AdvancedMath.gcd(12, 8), 4)
        self.assertEqual(AdvancedMath.gcd(100, 50), 50)
    
    def test_lcm(self):
        self.assertEqual(AdvancedMath.lcm(12, 8), 24)
        self.assertEqual(AdvancedMath.lcm(100, 50), 100)


class TestStringUtils(unittest.TestCase):
    """Test string utilities."""
    
    def test_case_conversion(self):
        self.assertEqual(StringUtils.uppercase("hello"), "HELLO")
        self.assertEqual(StringUtils.lowercase("HELLO"), "hello")
        self.assertEqual(StringUtils.capitalize("hello"), "Hello")
    
    def test_search(self):
        text = "The quick brown fox"
        self.assertTrue(StringUtils.startsWith(text, "The"))
        self.assertTrue(StringUtils.endsWith(text, "fox"))
        self.assertTrue(StringUtils.includes(text, "quick"))
        self.assertEqual(StringUtils.indexOf(text, "brown"), 10)
    
    def test_manipulation(self):
        self.assertEqual(StringUtils.substring("hello", 0, 3), "hel")
        self.assertEqual(StringUtils.replace("hello", "ll", "**"), "he**o")
        self.assertEqual(StringUtils.repeat("x", 3), "xxx")
        self.assertEqual(StringUtils.trim("  spaces  "), "spaces")
    
    def test_split(self):
        arr = StringUtils.split("a,b,c", ",")
        self.assertEqual(arr.length(), 3)
        self.assertEqual(arr.get(0), "a")


if __name__ == '__main__':
    unittest.main()
