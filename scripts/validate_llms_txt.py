#!/usr/bin/env python3
"""Validate llms.txt against v2 spec requirements."""

import re
from pathlib import Path
from typing import List, Tuple


class LlmsTxtValidator:
    """Validator for llms.txt v2 spec compliance."""

    LLMS_TXT_PATH = Path("docs/llms.md")

    def __init__(self):
        """Initialize validator."""
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self) -> bool:
        """Run all validations.

        Returns:
            True if all validations pass, False otherwise.
        """
        if not self.LLMS_TXT_PATH.exists():
            self.errors.append(f"File not found: {self.LLMS_TXT_PATH}")
            return False

        content = self.LLMS_TXT_PATH.read_text()

        self._validate_h1_title(content)
        self._validate_blockquote(content)
        self._validate_sections(content)
        self._validate_links(content)
        self._validate_structure(content)

        return len(self.errors) == 0

    def _validate_h1_title(self, content: str) -> None:
        """Validate H1 title exists."""
        lines = content.split("\n")
        if not lines or not lines[0].startswith("# "):
            self.errors.append("Missing H1 title (line must start with '# ')")

    def _validate_blockquote(self, content: str) -> None:
        """Validate blockquote summary exists."""
        lines = content.split("\n")
        found_blockquote = False
        for i, line in enumerate(lines[1:5], 1):  # Check first 5 lines
            if line.startswith("> "):
                found_blockquote = True
                break
        if not found_blockquote:
            self.errors.append("Missing blockquote summary (line starting with '> ')")

    def _validate_sections(self, content: str) -> None:
        """Validate required sections exist."""
        required_sections = [
            "Quick Start",
            "Core Concepts",
            "API Reference",
            "Error Handling",
        ]

        for section in required_sections:
            if f"## {section}" not in content:
                self.warnings.append(f"Missing section: '## {section}'")

    def _validate_links(self, content: str) -> None:
        """Validate links format and structure."""
        # Find all markdown links
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        links = re.findall(link_pattern, content)

        if not links:
            self.warnings.append("No links found in llms.txt")
            return

        for text, url in links:
            # Check for empty text
            if not text.strip():
                self.errors.append(f"Empty link text: [{text}]({url})")

            # Check for placeholder URLs
            if url in ["#", "TODO", ""] or url.startswith("http://"):
                self.warnings.append(f"Suspicious URL: [{text}]({url})")

    def _validate_structure(self, content: str) -> None:
        """Validate overall document structure."""
        # Should have H2 sections
        h2_count = content.count("\n## ")
        if h2_count < 3:
            self.warnings.append(f"Few H2 sections: only {h2_count} found")

        # Should have some links
        if content.count("](") < 5:
            self.warnings.append("Few links in document (expected at least 5)")

        # Check for common requirements
        if "API Reference" in content and "Error" not in content:
            self.warnings.append("API Reference section but no Error Handling section")

    def report(self) -> None:
        """Print validation report."""
        print("\n" + "=" * 80)
        print("llms.txt v2 Spec Validation Report")
        print("=" * 80)

        if not self.errors and not self.warnings:
            print("✅ All validations passed!")
            print(f"✅ {self.LLMS_TXT_PATH} is valid")
            return

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"   - {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   - {warning}")

        print("\n" + "=" * 80)


def main() -> int:
    """Run validation and return exit code."""
    validator = LlmsTxtValidator()
    is_valid = validator.validate()
    validator.report()

    return 0 if is_valid else 1


if __name__ == "__main__":
    exit(main())
