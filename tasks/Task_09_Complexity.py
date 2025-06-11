#!/usr/bin/env python3
"""
Task 09: Code Complexity and Readability Challenge

This file contains several intentional complexity and readability issues for code review practice.
The task is to identify and fix the following issues:
1. Complex nested conditionals in DataValidator
2. Long method with multiple responsibilities in ReportGenerator
3. Poor variable naming in DataProcessor
4. Complex data transformation in UserManager
5. Deep nesting in FileProcessor
6. Unclear business logic in OrderProcessor
7. Complex state management in CacheManager
8. Poor code organization in APIClient

Review the code and identify these complexity and readability issues.
"""

import json
import time
import random
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from pathlib import Path
import re
import hashlib
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataValidator:
    """
    Validates data according to complex rules.
    Bug: Complex nested conditionals and unclear validation logic.
    """
    def validate_data(self, data: Dict[str, Any], rules: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate data against rules."""
        errors = []
        # Bug: Complex nested conditionals
        if data is not None and isinstance(data, dict):
            for key, value in data.items():
                if key in rules:
                    rule = rules[key]
                    if isinstance(rule, dict):
                        if "type" in rule:
                            if rule["type"] == "string":
                                if not isinstance(value, str):
                                    errors.append(f"{key} must be a string")
                                elif "min_length" in rule and len(value) < rule["min_length"]:
                                    errors.append(f"{key} must be at least {rule['min_length']} characters")
                                elif "max_length" in rule and len(value) > rule["max_length"]:
                                    errors.append(f"{key} must be at most {rule['max_length']} characters")
                                elif "pattern" in rule and not re.match(rule["pattern"], value):
                                    errors.append(f"{key} must match pattern {rule['pattern']}")
                            elif rule["type"] == "number":
                                if not isinstance(value, (int, float)):
                                    errors.append(f"{key} must be a number")
                                elif "min" in rule and value < rule["min"]:
                                    errors.append(f"{key} must be at least {rule['min']}")
                                elif "max" in rule and value > rule["max"]:
                                    errors.append(f"{key} must be at most {rule['max']}")
                            elif rule["type"] == "array":
                                if not isinstance(value, list):
                                    errors.append(f"{key} must be an array")
                                elif "min_items" in rule and len(value) < rule["min_items"]:
                                    errors.append(f"{key} must have at least {rule['min_items']} items")
                                elif "max_items" in rule and len(value) > rule["max_items"]:
                                    errors.append(f"{key} must have at most {rule['max_items']} items")
                                elif "item_type" in rule:
                                    for i, item in enumerate(value):
                                        if not isinstance(item, eval(rule["item_type"])):
                                            errors.append(f"{key}[{i}] must be of type {rule['item_type']}")
                        elif "required" in rule and rule["required"] and value is None:
                            errors.append(f"{key} is required")
                    elif isinstance(rule, str):
                        if rule == "string" and not isinstance(value, str):
                            errors.append(f"{key} must be a string")
                        elif rule == "number" and not isinstance(value, (int, float)):
                            errors.append(f"{key} must be a number")
                        elif rule == "boolean" and not isinstance(value, bool):
                            errors.append(f"{key} must be a boolean")
        else:
            errors.append("Data must be a non-null dictionary")
        return len(errors) == 0, errors

class ReportGenerator:
    """
    Generates various types of reports.
    Bug: Long method with multiple responsibilities and complex logic.
    """
    def generate_report(self, data: List[Dict[str, Any]], report_type: str,
                       format_type: str = "text", include_summary: bool = True,
                       sort_by: Optional[str] = None, filter_criteria: Optional[Dict[str, Any]] = None,
                       group_by: Optional[str] = None, max_items: Optional[int] = None) -> str:
        """Generate a report from data."""
        # Bug: Long method with multiple responsibilities
        result = []
        processed_data = data.copy()

        # Filter data
        if filter_criteria:
            processed_data = [item for item in processed_data if all(
                item.get(k) == v for k, v in filter_criteria.items()
            )]

        # Sort data
        if sort_by:
            processed_data.sort(key=lambda x: x.get(sort_by, ""))

        # Group data
        if group_by:
            grouped_data = {}
            for item in processed_data:
                key = item.get(group_by, "unknown")
                if key not in grouped_data:
                    grouped_data[key] = []
                grouped_data[key].append(item)
            processed_data = grouped_data

        # Generate report content
        if report_type == "summary":
            if isinstance(processed_data, dict):
                for group, items in processed_data.items():
                    result.append(f"\nGroup: {group}")
                    result.append(self._generate_summary(items))
            else:
                result.append(self._generate_summary(processed_data))
        elif report_type == "detailed":
            if isinstance(processed_data, dict):
                for group, items in processed_data.items():
                    result.append(f"\nGroup: {group}")
                    result.extend(self._generate_detailed(items))
            else:
                result.extend(self._generate_detailed(processed_data))
        elif report_type == "statistical":
            if isinstance(processed_data, dict):
                for group, items in processed_data.items():
                    result.append(f"\nGroup: {group}")
                    result.append(self._generate_statistics(items))
            else:
                result.append(self._generate_statistics(processed_data))

        # Apply formatting
        if format_type == "html":
            result = self._format_html(result)
        elif format_type == "json":
            result = json.dumps({"report": result})
        elif format_type == "csv":
            result = self._format_csv(result)

        # Add summary if requested
        if include_summary:
            summary = self._generate_summary(data)
            if format_type == "html":
                result = f"<div class='summary'>{summary}</div>\n{result}"
            else:
                result = f"Summary:\n{summary}\n\n{result}"

        # Apply max items limit
        if max_items and isinstance(processed_data, list):
            result = result[:max_items]

        return "\n".join(result) if isinstance(result, list) else result

    def _generate_summary(self, data: List[Dict[str, Any]]) -> str:
        """Generate summary of data."""
        # Bug: Complex data aggregation
        if not data:
            return "No data available"

        total = len(data)
        numeric_fields = {}
        string_fields = {}

        for item in data:
            for key, value in item.items():
                if isinstance(value, (int, float)):
                    if key not in numeric_fields:
                        numeric_fields[key] = {"sum": 0, "count": 0, "min": float("inf"), "max": float("-inf")}
                    numeric_fields[key]["sum"] += value
                    numeric_fields[key]["count"] += 1
                    numeric_fields[key]["min"] = min(numeric_fields[key]["min"], value)
                    numeric_fields[key]["max"] = max(numeric_fields[key]["max"], value)
                elif isinstance(value, str):
                    if key not in string_fields:
                        string_fields[key] = {}
                    string_fields[key][value] = string_fields[key].get(value, 0) + 1

        summary = [f"Total items: {total}"]

        for field, stats in numeric_fields.items():
            avg = stats["sum"] / stats["count"]
            summary.append(f"{field}: min={stats['min']}, max={stats['max']}, avg={avg:.2f}")

        for field, counts in string_fields.items():
            most_common = max(counts.items(), key=lambda x: x[1])
            summary.append(f"{field}: most common value is '{most_common[0]}' ({most_common[1]} occurrences)")

        return "\n".join(summary)

    def _generate_detailed(self, data: List[Dict[str, Any]]) -> List[str]:
        """Generate detailed report."""
        # Bug: Complex formatting logic
        if not data:
            return ["No data available"]

        result = []
        headers = list(data[0].keys())
        max_lengths = {header: len(header) for header in headers}

        for item in data:
            for header in headers:
                max_lengths[header] = max(max_lengths[header], len(str(item.get(header, ""))))

        header_line = " | ".join(header.ljust(max_lengths[header]) for header in headers)
        separator = "-+-".join("-" * max_lengths[header] for header in headers)

        result.append(header_line)
        result.append(separator)

        for item in data:
            row = []
            for header in headers:
                value = str(item.get(header, ""))
                row.append(value.ljust(max_lengths[header]))
            result.append(" | ".join(row))

        return result

    def _generate_statistics(self, data: List[Dict[str, Any]]) -> str:
        """Generate statistical report."""
        # Bug: Complex statistical calculations
        if not data:
            return "No data available for statistical analysis"

        stats = {}
        for item in data:
            for key, value in item.items():
                if isinstance(value, (int, float)):
                    if key not in stats:
                        stats[key] = []
                    stats[key].append(value)

        result = []
        for field, values in stats.items():
            values.sort()
            n = len(values)
            mean = sum(values) / n
            median = values[n // 2] if n % 2 == 1 else (values[n // 2 - 1] + values[n // 2]) / 2
            variance = sum((x - mean) ** 2 for x in values) / n
            std_dev = variance ** 0.5

            result.append(f"{field}:")
            result.append(f"  Count: {n}")
            result.append(f"  Mean: {mean:.2f}")
            result.append(f"  Median: {median:.2f}")
            result.append(f"  Standard Deviation: {std_dev:.2f}")
            result.append(f"  Range: [{values[0]}, {values[-1]}]")

        return "\n".join(result)

    def _format_html(self, content: List[str]) -> str:
        """Format content as HTML."""
        # Bug: Complex HTML generation
        html = ["<table>"]
        for line in content:
            if line.startswith("Group:"):
                html.append(f"<tr><th colspan='100%'>{line}</th></tr>")
            elif "|" in line:
                cells = line.split("|")
                if any(cell.strip().startswith("-") for cell in cells):
                    html.append("<tr><td colspan='100%'><hr></td></tr>")
                else:
                    html.append("<tr>")
                    for cell in cells:
                        if cell.strip().startswith("Summary:"):
                            html.append(f"<td colspan='100%'><strong>{cell.strip()}</strong></td>")
                        else:
                            html.append(f"<td>{cell.strip()}</td>")
                    html.append("</tr>")
            else:
                html.append(f"<tr><td colspan='100%'>{line}</td></tr>")
        html.append("</table>")
        return "\n".join(html)

    def _format_csv(self, content: List[str]) -> str:
        """Format content as CSV."""
        # Bug: Complex CSV generation
        csv_lines = []
        for line in content:
            if "|" in line:
                cells = [cell.strip() for cell in line.split("|")]
                csv_lines.append(",".join(f'"{cell}"' for cell in cells))
            else:
                csv_lines.append(f'"{line}"')
        return "\n".join(csv_lines)

class DataProcessor:
    """
    Processes data with complex transformations.
    Bug: Poor variable naming and unclear data flow.
    """
    def __init__(self):
        # Bug: Unclear variable names
        self.x = {}
        self.y = []
        self.z = None

    def process(self, d: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process data with complex transformations."""
        # Bug: Poor variable names and complex logic
        r = []
        for i in d:
            t = {}
            for k, v in i.items():
                if isinstance(v, str):
                    t[k] = v.upper()
                elif isinstance(v, (int, float)):
                    t[k] = v * 2
                elif isinstance(v, list):
                    t[k] = [x for x in v if x is not None]
                elif isinstance(v, dict):
                    t[k] = {kk: vv for kk, vv in v.items() if vv is not None}
                else:
                    t[k] = v
            r.append(t)
        return r

class UserManager:
    """
    Manages user data and operations.
    Bug: Complex data transformation and unclear business logic.
    """
    def __init__(self):
        self.users = {}

    def process_user_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and transform user data."""
        # Bug: Complex data transformation
        processed = {}

        # Transform personal information
        if "personal_info" in user_data:
            pi = user_data["personal_info"]
            processed["name"] = f"{pi.get('first_name', '')} {pi.get('last_name', '')}".strip()
            processed["age"] = (datetime.now().year -
                              datetime.strptime(pi.get("birth_date", "2000-01-01"), "%Y-%m-%d").year)
            processed["email"] = pi.get("email", "").lower()
            processed["phone"] = re.sub(r"[^0-9+]", "", pi.get("phone", ""))

        # Transform address information
        if "address" in user_data:
            addr = user_data["address"]
            processed["address"] = {
                "street": addr.get("street", "").title(),
                "city": addr.get("city", "").title(),
                "state": addr.get("state", "").upper(),
                "zip": re.sub(r"[^0-9]", "", addr.get("zip", "")),
                "country": addr.get("country", "").title()
            }

        # Transform preferences
        if "preferences" in user_data:
            prefs = user_data["preferences"]
            processed["preferences"] = {
                "notifications": {
                    "email": prefs.get("notifications", {}).get("email", True),
                    "sms": prefs.get("notifications", {}).get("sms", False),
                    "push": prefs.get("notifications", {}).get("push", True)
                },
                "privacy": {
                    "profile_visible": prefs.get("privacy", {}).get("profile_visible", True),
                    "show_email": prefs.get("privacy", {}).get("show_email", False),
                    "show_phone": prefs.get("privacy", {}).get("show_phone", False)
                },
                "theme": prefs.get("theme", "light"),
                "language": prefs.get("language", "en")
            }

        # Transform security settings
        if "security" in user_data:
            sec = user_data["security"]
            processed["security"] = {
                "two_factor": sec.get("two_factor", False),
                "last_password_change": sec.get("last_password_change", datetime.now().isoformat()),
                "login_attempts": sec.get("login_attempts", 0),
                "account_locked": sec.get("login_attempts", 0) >= 3
            }

        # Transform activity data
        if "activity" in user_data:
            act = user_data["activity"]
            processed["activity"] = {
                "last_login": act.get("last_login", datetime.now().isoformat()),
                "login_count": act.get("login_count", 0),
                "posts": act.get("posts", []),
                "comments": act.get("comments", []),
                "likes": act.get("likes", []),
                "shares": act.get("shares", [])
            }

        return processed

class FileProcessor:
    """
    Processes files with complex operations.
    Bug: Deep nesting and complex control flow.
    """
    def process_file(self, filepath: str, operations: List[str]) -> bool:
        """Process a file with multiple operations."""
        # Bug: Deep nesting and complex control flow
        try:
            with open(filepath, 'r') as f:
                content = f.read()

                if "compress" in operations:
                    if len(content) > 1000:
                        content = self._compress_content(content)
                    else:
                        logger.warning("Content too small to compress")

                if "encrypt" in operations:
                    if not self._is_encrypted(content):
                        content = self._encrypt_content(content)
                    else:
                        logger.warning("Content already encrypted")

                if "validate" in operations:
                    if not self._validate_content(content):
                        logger.error("Content validation failed")
                        return False

                if "transform" in operations:
                    if self._needs_transformation(content):
                        content = self._transform_content(content)
                    else:
                        logger.info("No transformation needed")

                if "sanitize" in operations:
                    if self._contains_sensitive_data(content):
                        content = self._sanitize_content(content)
                    else:
                        logger.info("No sanitization needed")

                with open(filepath, 'w') as f:
                    f.write(content)

                return True
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return False

    def _compress_content(self, content: str) -> str:
        """Compress content."""
        # Bug: Complex compression logic
        return content[:len(content)//2]  # Simplified compression

    def _encrypt_content(self, content: str) -> str:
        """Encrypt content."""
        # Bug: Complex encryption logic
        return hashlib.md5(content.encode()).hexdigest()  # Simplified encryption

    def _is_encrypted(self, content: str) -> bool:
        """Check if content is encrypted."""
        return len(content) == 32 and all(c in "0123456789abcdef" for c in content)

    def _validate_content(self, content: str) -> bool:
        """Validate content."""
        return len(content) > 0 and not content.isspace()

    def _needs_transformation(self, content: str) -> bool:
        """Check if content needs transformation."""
        return any(c.isupper() for c in content)

    def _transform_content(self, content: str) -> str:
        """Transform content."""
        return content.lower()

    def _contains_sensitive_data(self, content: str) -> bool:
        """Check if content contains sensitive data."""
        patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # email
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # phone
            r'\b\d{16}\b'  # credit card
        ]
        return any(re.search(pattern, content) for pattern in patterns)

    def _sanitize_content(self, content: str) -> str:
        """Sanitize content."""
        # Bug: Complex sanitization logic
        content = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', content)
        content = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE]', content)
        content = re.sub(r'\b\d{16}\b', '[CREDIT_CARD]', content)
        return content

def main():
    # Test DataValidator complex conditionals
    print("Testing DataValidator complex conditionals:")
    validator = DataValidator()
    data = {
        "name": "John Doe",
        "age": 25,
        "email": "john@example.com",
        "scores": [85, 90, 95]
    }
    rules = {
        "name": {"type": "string", "min_length": 3, "max_length": 50},
        "age": {"type": "number", "min": 18, "max": 100},
        "email": {"type": "string", "pattern": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'},
        "scores": {"type": "array", "min_items": 1, "max_items": 5, "item_type": "int"}
    }
    is_valid, errors = validator.validate_data(data, rules)
    print(f"Validation result: {is_valid}")
    print(f"Errors: {errors}")

    # Test ReportGenerator long method
    print("\nTesting ReportGenerator long method:")
    generator = ReportGenerator()
    data = [
        {"name": "John", "age": 30, "score": 85},
        {"name": "Jane", "age": 25, "score": 90},
        {"name": "Bob", "age": 35, "score": 95}
    ]
    report = generator.generate_report(
        data,
        report_type="detailed",
        format_type="html",
        include_summary=True,
        sort_by="score",
        group_by="age"
    )
    print(f"Generated report:\n{report}")

    # Test DataProcessor poor naming
    print("\nTesting DataProcessor poor naming:")
    processor = DataProcessor()
    data = [
        {"name": "John", "age": 30, "scores": [85, 90, None, 95]},
        {"name": "Jane", "age": 25, "scores": [90, None, 95]}
    ]
    result = processor.process(data)
    print(f"Processed data: {result}")

    # Test UserManager complex transformation
    print("\nTesting UserManager complex transformation:")
    manager = UserManager()
    user_data = {
        "personal_info": {
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "1990-01-01",
            "email": "JOHN@example.com",
            "phone": "(123) 456-7890"
        },
        "address": {
            "street": "123 main st",
            "city": "new york",
            "state": "ny",
            "zip": "10001",
            "country": "usa"
        },
        "preferences": {
            "notifications": {"email": True, "sms": False},
            "privacy": {"profile_visible": True, "show_email": False},
            "theme": "dark",
            "language": "en"
        }
    }
    processed = manager.process_user_data(user_data)
    print(f"Processed user data: {processed}")

    # Test FileProcessor deep nesting
    print("\nTesting FileProcessor deep nesting:")
    processor = FileProcessor()
    test_file = "test.txt"
    try:
        with open(test_file, "w") as f:
            f.write("Test content with UPPERCASE and email@example.com and 123-456-7890")
        result = processor.process_file(test_file, ["compress", "encrypt", "validate", "transform", "sanitize"])
        print(f"File processing result: {result}")
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    main()