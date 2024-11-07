#!/usr/bin/env python3
"""
Main file
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Redacts specified fields in a log message.

    Parameters:
    - fields: List of strings with field names to redact.
    - redaction: The string to replace sensitive information with.
    - message: The log message containing sensitive information.
    - separator: The character separating fields in the message.

    Returns:
    A new message with specified fields redacted.
    """
    return re.sub(
        rf"({'|'.join(map(re.escape, fields))})=[^ {separator}]+",
        lambda match: f"{match.group(1)}={redaction}",
        message
    )


def main():
    message = "name=John Doe;email=john.doe@example.com;phone=123-456-7890"
    fields = ["name", "email", "phone"]
    redacted_message = filter_datum(fields, "REDACTED", message, ";")
    print(redacted_message)


if __name__ == "__main__":
    main()
