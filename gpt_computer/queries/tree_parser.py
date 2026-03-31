"""
Tree-sitter based code parser for extracting structural information from source code.

This module provides functionality to parse various programming languages using tree-sitter
and extract code structure elements like functions, classes, variables, and imports.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import tree_sitter

from gpt_computer.tools.supported_languages import SUPPORTED_LANGUAGES


class TreeParser:
    """Tree-sitter based code parser."""

    def __init__(self):
        """Initialize the tree parser with language parsers."""
        self.parsers: Dict[str, Any] = {}
        self.queries: Dict[str, Any] = {}
        self._load_languages()

    def _load_languages(self):
        """Load tree-sitter language parsers and queries."""
        base_dir = Path(__file__).parent

        for language in SUPPORTED_LANGUAGES:
            tree_sitter_name = language["tree_sitter_name"]

            try:
                # Import the language module
                language_module = __import__(
                    f"tree_sitter_{tree_sitter_name}", fromlist=[tree_sitter_name]
                )
                language_class = getattr(language_module, "language")

                # Create parser
                parser = tree_sitter.Parser()
                parser.set_language(language_class)
                self.parsers[tree_sitter_name] = parser

                # Load query file if it exists
                query_file = (
                    base_dir / "tree-sitter-language-pack" / f"{tree_sitter_name}.scm"
                )
                if query_file.exists():
                    with open(query_file, "r", encoding="utf-8") as f:
                        query_text = f.read()
                    query = language_class.query(query_text)
                    self.queries[tree_sitter_name] = query

            except (ImportError, AttributeError):
                # Language not available, skip it
                continue

    def get_supported_languages(self) -> List[str]:
        """Get list of supported tree-sitter languages."""
        return list(self.parsers.keys())

    def parse_file(self, file_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Parse a source code file and extract structural information.

        Args:
            file_path: Path to the source code file

        Returns:
            Dictionary containing extracted code elements
        """
        file_path = Path(file_path)

        # Determine language from file extension
        language = self._detect_language(file_path)
        if not language:
            return {"error": f"Unsupported file type: {file_path.suffix}"}

        if language not in self.parsers:
            return {"error": f"Tree-sitter parser not available for: {language}"}

        try:
            # Read file content
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()

            return self.parse_code(source_code, language)

        except Exception as e:
            return {"error": f"Failed to parse file {file_path}: {str(e)}"}

    def parse_code(
        self, source_code: str, language: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Parse source code string and extract structural information.

        Args:
            source_code: Source code to parse
            language: Programming language name

        Returns:
            Dictionary containing extracted code elements
        """
        if language not in self.parsers:
            return {"error": f"Tree-sitter parser not available for: {language}"}

        parser = self.parsers[language]

        try:
            # Parse the source code
            tree = parser.parse(bytes(source_code, "utf-8"))

            # Extract information using queries if available
            if language in self.queries:
                return self._extract_with_queries(tree, language)
            else:
                return self._extract_basic_info(tree, source_code)

        except Exception as e:
            return {"error": f"Failed to parse code: {str(e)}"}

    def _detect_language(self, file_path: Path) -> Optional[str]:
        """Detect programming language from file extension."""
        extension = file_path.suffix.lower()

        for language in SUPPORTED_LANGUAGES:
            if extension in language["extensions"]:
                return language["tree_sitter_name"]

        return None

    def _extract_with_queries(
        self, tree: Any, language: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Extract code information using tree-sitter queries."""
        query = self.queries[language]
        captures = query.captures(tree.root_node)

        result = {
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "calls": [],
            "other": [],
        }

        for capture in captures:
            node, capture_name = capture

            element = {
                "name": self._get_node_text(node),
                "type": capture_name,
                "line": node.start_point[0] + 1,
                "column": node.start_point[1] + 1,
                "end_line": node.end_point[0] + 1,
                "end_column": node.end_point[1] + 1,
            }

            # Categorize based on capture name
            if "function" in capture_name:
                result["functions"].append(element)
            elif "class" in capture_name:
                result["classes"].append(element)
            elif "variable" in capture_name:
                result["variables"].append(element)
            elif "import" in capture_name:
                result["imports"].append(element)
            elif "call" in capture_name:
                result["calls"].append(element)
            else:
                result["other"].append(element)

        return result

    def _extract_basic_info(
        self, tree: Any, source_code: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Extract basic information without specific queries."""
        result = {
            "functions": [],
            "classes": [],
            "variables": [],
            "imports": [],
            "calls": [],
            "other": [],
        }

        # Basic traversal to find common patterns
        def traverse(node):
            if node.type in [
                "function_definition",
                "function_declaration",
                "method_definition",
            ]:
                result["functions"].append(
                    {
                        "name": self._get_node_text(node),
                        "type": node.type,
                        "line": node.start_point[0] + 1,
                        "column": node.start_point[1] + 1,
                    }
                )
            elif node.type in ["class_definition", "class_declaration"]:
                result["classes"].append(
                    {
                        "name": self._get_node_text(node),
                        "type": node.type,
                        "line": node.start_point[0] + 1,
                        "column": node.start_point[1] + 1,
                    }
                )
            elif node.type in ["import_statement", "import_declaration"]:
                result["imports"].append(
                    {
                        "name": self._get_node_text(node),
                        "type": node.type,
                        "line": node.start_point[0] + 1,
                        "column": node.start_point[1] + 1,
                    }
                )

            for child in node.children:
                traverse(child)

        traverse(tree.root_node)
        return result

    def _get_node_text(self, node: Any) -> str:
        """Extract text content from a tree-sitter node."""
        return node.text.decode("utf-8")


# Global instance
tree_parser = TreeParser()


def parse_file(file_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse a source code file and extract structural information.

    Args:
        file_path: Path to the source code file

    Returns:
        Dictionary containing extracted code elements
    """
    return tree_parser.parse_file(file_path)


def parse_code(source_code: str, language: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse source code string and extract structural information.

    Args:
        source_code: Source code to parse
        language: Programming language name

    Returns:
        Dictionary containing extracted code elements
    """
    return tree_parser.parse_code(source_code, language)


def get_supported_languages() -> List[str]:
    """Get list of supported tree-sitter languages."""
    return tree_parser.get_supported_languages()
