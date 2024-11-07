#!/usr/bin/env python3
"""
Filtered Logger Module
"""

import os
import mysql.connector
import logging
from typing import List
import bcrypt
import re

# Fetch database credentials from environment variables
DB_USERNAME = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
DB_PASSWORD = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
DB_HOST = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
DB_NAME = os.getenv("PERSONAL_DATA_DB_NAME")

# Fields to redact from the logs
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_db():
    """
    Returns a connection to the MySQL database using credentials from 
    environment variables.
    """
    try:
        connection = mysql.connector.connect(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def filter_datum(fields: List[str], redaction: str, message: str, 
                 separator: str) -> str:
    """
    Redacts specified fields in a log message.
    """
    return re.sub(
        rf"({'|'.join(map(re.escape, fields))})=[^ {separator}]+",
        lambda match: f"{match.group(1)}={redaction}",
        message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.message = filter_datum(self.fields, self.REDACTION, 
                                      record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger with RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # Do not propagate messages to other loggers
    
    # Create a stream handler and set the formatter
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    
    # Add the handler to the logger
    logger.addHandler(handler)
    
    return logger


def main():
    """
    Main function to fetch users from the database and log their data in 
    a filtered format.
    """
    db = get_db()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users;")
        for row in cursor:
            user_data = {
                "name": row[0],
                "email": row[1],
                "phone": row[2],
                "ssn": row[3],
                "password": row[4],
                "ip": row[5],
                "last_login": row[6],
                "user_agent": row[7]
            }
            logger = get_logger()
            logger.info(f"name={user_data['name']}; email={user_data['email']}; "
                        f"phone={user_data['phone']}; ssn={user_data['ssn']}; "
                        f"password={user_data['password']}; ip={user_data['ip']}; "
                        f"last_login={user_data['last_login']}; "
                        f"user_agent={user_data['user_agent']};")
        cursor.close()
        db.close()
    else:
        print("Failed to connect to the database.")


if __name__ == "__main__":
    main()
