#!/usr/bin/env python3
"""
function called filter_datum
that returns the log message obfuscated:
"""
from typing import List
import re


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    uses regex to redact sensitve
    information from a log message
    """
    for i in fields:
        message = re.sub(f"{i}=.*?{separator}",
                         f"{i}={redaction}{separator}", message)
    return message
