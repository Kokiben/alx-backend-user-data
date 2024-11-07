#!/usr/bin/env python3
"""
Main file
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    return re.sub(
        rf"({'|'.join(fields)})=[^ {separator}]+",
        lambda match: f"{match.group(1)}={redaction}",
        message
    )


# Example usage
if __name__ == "__main__":
    main()
