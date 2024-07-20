import mysql.connector as sql
import logging
from logging_setup import setup_logging

setup_logging(log_file="logs/db_connection.log", level=logging.DEBUG)

try:
    lol_db = sql.connect(
        host="localhost",
        user="root",
        password="root",
        database="lol_player_stats"
    )


    logging.debug("Connection successful!")

except sql.Error as err:
    logging.error(f"Error connecting to database: {err}")

finally:
    lol_db.close()
    logging.debug("Connection closed.")