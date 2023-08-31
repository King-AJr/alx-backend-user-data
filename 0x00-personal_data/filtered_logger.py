#!/usr/bin/env python3
"""
function called filter_datum
that returns the log message obfuscated:
"""
from typing import List
import re
import logging


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """
        initialize arguments
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format records by redacting sensitive info
        """
        return super(RedactingFormatter, self).format(record)
