import mysql.connector as sql
import logging
import json
from logging_setup import setup_logging

# Logging setup
setup_logging(log_file="logs/db_data_adder.log", level=logging.DEBUG)

# SQL connection to the lol_player_stats DB
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



# Extract the JSON data for the Summoners table of the DB
def extract_summoners_data_from_json(file_path: str) -> dict: 
    # Open the JSON file
    try:
        with open(file_path, "r") as json_file:
            summoner_data = json.load(json_file)
            logging.info("JSON file opened successfully.")
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {file_path}")
        raise

    info_query = (
        summoner_data['id'], 
        summoner_data["summoner_id"], 
        summoner_data['region'], 
        summoner_data['account_id'], 
        summoner_data['puuid'],
        summoner_data['game_name'],
        summoner_data['tagline'],
        summoner_data['name'],
        summoner_data['internal_name'],
        summoner_data['profile_image_url'],
        summoner_data['level'],
        summoner_data['updated_at'],
        summoner_data['renewable_at'],
    )

    return info_query

# Construct query for the MySQL DB
def insert_data_summoners_table(file_path: str)-> str:

    summoners_data = extract_summoners_data_from_json(file_path)

    cursor = lol_db.cursor()

    # Construct the query
    query = """
        INSERT INTO Summoners (
            id,
            summoner_id, 
            region, 
            account_id, 
            puuid, 
            game_name, 
            tagline, 
            name_,
            internal_name, 
            profile_icon_url, 
            level, 
            updated_at, 
            renewable_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Execute the query
    try:
        cursor.execute(query, summoners_data)
        lol_db.commit()
        logging.info("Data inserted into Summoners table successfully.")
    except sql.Error as err:
        logging.error(f"Error inserting data into Summoners table: {err}")
        lol_db.rollback()

    return(cursor.rowcount, "record inserted.")


if __name__ == "__main__":
    file_path = "summoner_data_souvenir#2310.json"
    insert_data_summoners_table(file_path)




