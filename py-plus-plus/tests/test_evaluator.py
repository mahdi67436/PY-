"""Tests for evaluator."""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interpreter import interpret

class TestEvaluator(unittest.TestCase):
    
    def test_arithmetic(self):
        # Capture print output for testing
        import io
        from contextlib import redirect_stdout
        
        code = "print(2 + 3);"
        f = io.StringIO()
        with redirect_stdout(f):
            interpret(code)
        assert "5" in f.getvalue()
    
    def test_variable_assignment(self):
        code = """
        let x = 10;
        let y = x + 5;
        print(y);
        """
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            interpret(code)
        assert "15" in f.getvalue()
    
    def test_function_call(self):
        code = """
        fn double(x) { return x * 2; }
        print(double(5));
        """
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            interpret(code)
        assert "10" in f.getvalue()
    
    def test_if_statement(self):
        code = """
        let x = 10;
        if (x > 5) { print("big"); } else { print("small"); }
        """
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            interpret(code)
        assert "big" in f.getvalue()
    
    def test_loop(self):
        code = """
        for (let i = 0; i < 3; i = i + 1) {
            print(i);
        }
        """
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            interpret(code)
        output = f.getvalue()
        assert "0" in output
        assert "1" in output
        assert "2" in output

if __name__ == '__main__':
    unittest.main()
