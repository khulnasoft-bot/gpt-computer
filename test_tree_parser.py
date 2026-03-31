#!/usr/bin/env python3
"""
Simple test script for tree-sitter parser implementation.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "gpt_computer"))

# Import after path setup
# ruff: noqa: E402
from gpt_computer.queries.tree_parser import get_supported_languages, parse_code


def test_parser():
    """Test the tree-sitter parser with sample code."""

    print("Supported languages:", get_supported_languages())

    # Test Python code
    python_code = '''
def hello_world():
    """A simple hello world function."""
    print("Hello, World!")

class MyClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

import os
from typing import List
'''

    print("\n=== Parsing Python Code ===")
    result = parse_code(python_code, "python")
    for key, values in result.items():
        if values and key != "error":
            print(f"{key.capitalize()}:")
            for item in values:
                print(f"  - {item['name']} (line {item.get('line', 'N/A')})")

    # Test JavaScript code
    js_code = """
function greet(name) {
    return `Hello, ${name}!`;
}

class Person {
    constructor(name) {
        this.name = name;
    }

    sayHello() {
        return greet(this.name);
    }
}

import { useState } from 'react';
"""

    print("\n=== Parsing JavaScript Code ===")
    result = parse_code(js_code, "javascript")
    for key, values in result.items():
        if values and key != "error":
            print(f"{key.capitalize()}:")
            for item in values:
                print(f"  - {item['name']} (line {item.get('line', 'N/A')})")


if __name__ == "__main__":
    test_parser()
