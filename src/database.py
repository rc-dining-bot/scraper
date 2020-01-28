import os
import psycopg2
from psycopg2.extras import execute_values
import logging
import sys

from queries import (breakfast_insert_query, breakfast_insert_template,
                     dinner_insert_query, dinner_insert_template)

# global singleton connection
_connection = None


def connect():
    """ Connect to the PostgreSQL database server"""
    global _connection
    # if connection is already formed, return connection
    if _connection:
        return _connection

    try:
        # connect to the PostgreSQL server
        logging.info("Connecting to the PostgreSQL database...")
        _connection = psycopg2.connect(host=os.getenv("RC_DINING_BOT_HOST"),
                                       database=os.getenv(
                                           "RC_DINING_BOT_DATABASE"),
                                       user=os.getenv("RC_DINING_BOT_DB_USER"),
                                       password=os.getenv("RC_DINING_BOT_DB_PASSWORD"))

        # create a cursor
        cursor = _connection.cursor()

        # display the PostgreSQL database server version
        logging.info("PostgreSQL database version:")
        cursor.execute("SELECT version()")
        db_version = cursor.fetchone()
        logging.info(db_version)

        cursor.close()
    except Exception as error:
        logging.fatal(error)
        sys.exit(1)


def breakfast_insert_many(ops):
    conn = connect()
    cur = conn.cursor()
    execute_values(cur, breakfast_insert_query,
                   ops, breakfast_insert_template)
    conn.commit()
    cur.close()
    logging.info('Inserted to breakfast successfully')


def dinner_insert_many(ops):
    conn = connect()
    cur = conn.cursor()
    execute_values(cur, dinner_insert_query,
                   ops, dinner_insert_template)
    conn.commit()
    cur.close()
    logging.info('Inserted to dinner successfully')
