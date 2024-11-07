#!/usr/bin/env python3
"""
Personal Data Processing Script
"""

import logging
import os
import re
from typing import List
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def redact_data(fields: List[str], redaction: str, log_message: str,
                separator: str) -> str:
    """ Redacts sensitive information in the log message. """
    for field in fields:
        log_message = re.sub(rf"{field}=(.*?)\{separator}",
                             f'{field}={redaction}{separator}', log_message)
    return log_message


class RedactingFormatter(logging.Formatter):
    """ Formatter class that redacts PII from log messages. """

    REDACTION = "***"
    FORMAT = "[USER_DATA] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initializes RedactingFormatter with specified PII fields. """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """ Redacts the message fields before formatting the log record. """
        return redact_data(self.fields, self.REDACTION,
                           super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ Initializes and returns a logger instance. """

    logger = logging.getLogger("user_data_logger")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def connect_to_db() -> mysql.connector.connection.MySQLConnection:
    """ Establishes a connection to the database. """

    db_password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_username = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    db_host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.environ.get('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_username,
        password=db_password)
    return connection


def main() -> None:
    """ Main function that retrieves and prints user data from database. """
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        log_message = f"name={row[0]}; email={row[1]}; phone={row[2]}; " +\
            f"ssn={row[3]}; password={row[4]};ip={row[5]}; " +\
            f"last_login={row[6]}; user_agent={row[7]};"
        print(log_message)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
