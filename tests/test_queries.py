import mysql.connector as sql
import logging

import sys
sys.path.append('..')
from logging_setup import setup_logging

# Logging setup
setup_logging(log_file="../logs/list_best_champs.log", level=logging.DEBUG)

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

# Create a cursor object
cursor = lol_db.cursor()

def test_query1()-> None:
   
    query_players_names = """
            SELECT DISTINCT champion_stats.player_id, summoners.name_
            FROM summoners
            LEFT JOIN champion_stats 
                ON summoners.opgg_id = champion_stats.player_id;
        """
    cursor.execute(query_players_names)

    try:
        player_data = cursor.fetchall()
        
    except Exception as err:
        logging.error(f"Error fetching player data: {err}")
  
    print("Player Names and IDs:")
    for row in player_data:
        print(f'Player ID: {row[0]}\tPlayer Name: {row[1]}')

def test_query2() -> None:

    # Add the , to make python think it is a tuple
    player_id: tuple[str] = ("136730552",)

    query_ordered_list_champs = """
        SELECT champion, win, lose, winrate, kda
        FROM champion_stats
        WHERE player_id = %s
        ORDER BY winrate DESC, kda DESC;
    """
    cursor.execute(query_ordered_list_champs, player_id)

    try:
        champion_data = cursor.fetchall()
    except Exception as err:
        logging.error(f"Error fetching champion data {err}")

    for row in champion_data:
        print(f"Champion: {row[0]}\t Wins: {row[1]}\t Losses: {row[2]}\t Winrate: {row[3]}\t KDA: {row[4]}")


if __name__ == "__main__":

    test_query1()
    test_query2()
