import mysql.connector as sql
import logging
import pandas as pd

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

def insert_name(username)-> str:
   
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
  
    try:
        for player_id, name in player_data:
            if name == username:
                return player_id, name
    except:
        logging.error(f"Error finding username in player data: {username}")

    

def extract_champions_data(id) -> list:

    # Add the , to make python think it is a tuple
    player_id: tuple[str] = (id,)

    query_ordered_list_champs = """
        SELECT id, champion, win, lose, winrate, kda
        FROM champion_stats
        WHERE player_id = %s
        ORDER BY winrate DESC, kda DESC;
    """
    cursor.execute(query_ordered_list_champs, player_id)

    try:
        champion_data = cursor.fetchall()
    except Exception as err:
        logging.error(f"Error fetching champion data {err}")

    return champion_data

def transform_champions_data(champion_data: list) -> None:

    df = pd.DataFrame(champion_data, columns=['id', 'champions_name', 'nbr_of_wins', 'nbr_of_losses', 'winrate', 'KDA'])

    # We keep the id to make sure that the oldest data is dropped
    df = df.drop_duplicates(ignore_index=True, keep='last', subset=['champions_name', 'nbr_of_wins', 'nbr_of_losses', 'winrate', 'KDA'])

    df.dropna(inplace=True)

    return df

def load_champions_data(name, df)-> None:

    filame = f"champions_data_{name}"
    try:
        df.to_csv(filame, sep=',', index=False)
        logging.info(f"csv data saved to {filame}")
    except Exception as err:
        logging.error(f"Error saving data to csv: {err}")

def ETL_pipeline_champions_data()-> None:

    champion_data = extract_champions_data(id)
    df =transform_champions_data(champion_data)
    load_champions_data(name, df)

def test_season_data(id)-> str:

    # Add the , to make python think it is a tuple
    player_id: tuple[str] = (id,)

    query_test = """
    SELECT *, (win + lose) AS number_of_games_played
	FROM league_stats
    WHERE player_id = %s;
    """

    # Idea of transformation that could be added:
    # The number of lps that are needed to go to the next tier if not unranked
    # if unranked the number of games left to play to get ranked

    cursor.execute(query_test, player_id)

    try:
        season_data = cursor.fetchall()
    except Exception as err:
        logging.error(f"Error fetching season data {err}")

    return season_data

if __name__ == "__main__":
    id, name = insert_name("souvenir13")
    #ETL_pipeline_champions_data()

    test = test_season_data(id)

    print(test)
