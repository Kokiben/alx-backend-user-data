#!/usr/bin/env python3
"""
Data Processing Script
"""

import logging
import os
import re
from typing import List
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Redacts sensitive information in the log message. """
    for fld in fields:
        message = re.sub(rf"{fld}=(.*?)\{separator}",
                         f'{fld}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Formatter class that redacts PII from log messages."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Init """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Initializes RedactingFormatter with specified PII fields. """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Initializes and returns a logger instance.
    """

    user_logger = logging.getLogger("user_data")
    user_logger.setLevel(logging.INFO)
    user_logger.propagate = False
    user_handler = logging.StreamHandler()
    user_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    user_logger.addHandler(user_handler)
    return user_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Establishes a connection to the database.
    """
    db_paswd = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_nm = os.environ.get('PERSONAL_DATA_DB_NAME')
    conection = mysql.connector.connect(
        host=db_host,
        database=db_nm,
        user=db_username,
        password=db_paswd)
    return conection


def main() -> None:
    """ Main function that retrieves and prints user data from database.
    """
    datab = get_db()
    db_cursor = datab.cursor()
    db_cursor.execute("SELECT * FROM users;")
    for us_rw in db_cursor:
        message = f"name={us_rw[0]}; email={us_rw[1]}; phone={us_rw[2]}; " +\
            f"ssn={us_rw[3]}; password={us_rw[4]};ip={us_rw[5]}; " +\
            f"last_login={us_rw[6]}; user_agent={us_rw[7]};"
        print(message)
    db_cursor.close()
    datab.close()


if __name__ == '__main__':
    main()
