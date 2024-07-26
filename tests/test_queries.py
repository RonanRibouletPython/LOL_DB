import mysql.connector as sql
import logging
import pandas as pd

from datetime import datetime 

import sys
sys.path.append('..')
from logging_setup import setup_logging

# Logging setup
setup_logging(log_file="../logs/list_best_champs.log", level=logging.DEBUG)

import requests
from PIL import Image
import io

def img_download_from_url(url: str, filename: str) -> None:
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        img = Image.open(io.BytesIO(response.content))
        img.save(filename)
        logging.info(f'Image sucessfully downloaded and saved: {filename}')
    else:
        logging.error(f"Error downloading image from url: {url}")

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
    
    return None

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

    filame = f"champions_data_{name}.csv"
    try:
        df.to_csv(filame, sep=',', index=False)
        logging.info(f"csv data saved to {filame}")
    except Exception as err:
        logging.error(f"Error saving data to csv: {err}")
    
    return None

def ETL_pipeline_champions_data()-> None:

    champion_data = extract_champions_data(id)
    df =transform_champions_data(champion_data)
    load_champions_data(name, df)

    return None

def extract_season_data(id)-> str:

    # Add the , to make python think it is a tuple
    player_id: tuple[str] = (id,)

    query_season_data = """
        SELECT id, player_id, queue_type, tier, division, lp, win, lose, winrate, (win + lose) AS number_of_games_played
        FROM league_stats
        WHERE player_id = %s;
    """

    # Idea of transformation that could be added:
    # The number of lps that are needed to go to the next tier if not unranked
    # if unranked the number of games left to play to get ranked

    cursor.execute(query_season_data, player_id)

    try:
        season_data = cursor.fetchall()
    except Exception as err:
        logging.error(f"Error fetching season data {err}")

    return season_data

def transform_season_data(season_data: list) -> None:

    df = pd.DataFrame(season_data, columns=['id', 'player_id', 'queue_type', 'tier', 'division', 'lp', 'win', 'lose', 'winrate', 'number_of_games_played'])

    # We keep the id to make sure that the oldest data is dropped
    df = df.drop_duplicates(ignore_index=True, keep='last', subset=['player_id', 'queue_type'])

    df.dropna(inplace=True)

    return df

def load_season_data(name, df)-> None:

    filame = f"season_data_{name}.csv"
    try:
        df.to_csv(filame, sep=',', index=False)
        logging.info(f"csv data saved to {filame}")
    except Exception as err:
        logging.error(f"Error saving data to csv: {err}")
    
    return None

def ETL_pipeline_season_data()-> None:

    champion_data = extract_season_data(id)
    df =transform_season_data(champion_data)
    load_season_data(name, df)

    return None

def extract_summoner_data(id)-> str:

    # Add the , to make python think it is a tuple
    player_id: tuple[str] = (id,)

    query_summoner_data = '''
        SELECT id, opgg_id, region, name_, profile_icon_url, level, updated_at
        FROM summoners
        WHERE opgg_id = %s;
    '''

    # Idea of transformation that could be added:
    # The number of lps that are needed to go to the next tier if not unranked
    # if unranked the number of games left to play to get ranked

    cursor.execute(query_summoner_data, player_id)

    try:
        summoner_data = cursor.fetchall()
    except Exception as err:
        logging.error(f"Error fetching season data {err}")

    return summoner_data

def transform_summoner_data(season_data: list) -> None:

    df = pd.DataFrame(season_data, columns=['id', 'opgg_id', 'region', 'name_', 'profile_icon_url', 'level', 'updated_at'])

    # We keep the id to make sure that the oldest data is dropped
    df = df.drop_duplicates(ignore_index=True, keep='last', subset=['name_'])

    df.dropna(inplace=True)

    return df

def load_summoner_data(name, df)-> None:

    filame = f"summoner_data_{name}.csv"
    try:
        df.to_csv(filame, sep=',', index=False)
        logging.info(f"csv data saved to {filame}")
    except Exception as err:
        logging.error(f"Error saving data to csv: {err}")
    
    return None

def ETL_pipeline_summoner_data()-> None:

    champion_data = extract_summoner_data(id)
    df =transform_summoner_data(champion_data)
    load_summoner_data(name, df)

    return None

def extract_season_history_data(id)-> str:

    # Add the , to make python think it is a tuple
    player_id: tuple[str] = (id,)

    query_season_history = '''
        SELECT id, player_id, season, tier, division, lp
        FROM season_history
        WHERE player_id = %s;
    '''

    # Idea of transformation that could be added:
    # The number of lps that are needed to go to the next tier if not unranked
    # if unranked the number of games left to play to get ranked

    cursor.execute(query_season_history, player_id)

    try:
        season_history_data = cursor.fetchall()
    except Exception as err:
        logging.error(f"Error fetching season data {err}")

    return season_history_data

def transform_season_history_data(season_history_data: list) -> None:

    df = pd.DataFrame(season_history_data, columns=['id', 'player_id', 'season', 'tier', 'division', 'lp'])

    # We keep the id to make sure that the oldest data is dropped
    df = df.drop_duplicates(ignore_index=True, keep='last', subset=['player_id', 'season'])

    # Delete the current season because it should not be stored in a historic of previous seasons
    index_current_season = df[(df['season'] == datetime.now().year)].index
    df.drop(index_current_season, inplace=True)

    df.dropna(inplace=True)

    return df

def load_season_history_data(name, df)-> None:

    filame = f"season_history_data_{name}.csv"
    try:
        df.to_csv(filame, sep=',', index=False)
        logging.info(f"csv data saved to {filame}")
    except Exception as err:
        logging.error(f"Error saving data to csv: {err}")
    
    return None

def ETL_pipeline_season_history_data()-> None:

    champion_data = extract_season_history_data(id)
    df =transform_season_history_data(champion_data)
    load_season_history_data(name, df)

    return None

def extract_recent_games_data(id)-> str:

    # Add the , to make python think it is a tuple
    player_id: tuple[str] = (id,)

    query_recent_games = '''
        SELECT id, player_id, champion, kill_, death, assist, position, is_win 
        FROM recent_game_stats
        WHERE player_id = %s;
    '''

    # Idea of transformation that could be added:
    # The number of lps that are needed to go to the next tier if not unranked
    # if unranked the number of games left to play to get ranked

    cursor.execute(query_recent_games, player_id)

    try:
        recent_games_data = cursor.fetchall()
    except Exception as err:
        logging.error(f"Error fetching season data {err}")

    return recent_games_data

def transform_recent_games_data(recent_games_data: list) -> None:

    df = pd.DataFrame(recent_games_data, columns=['id', 'player_id', 'champion', 'kill_', 'death', 'assist', 'position', 'is_win'])

    # We keep the id to make sure that the oldest data is dropped
    df = df.drop_duplicates(ignore_index=True, keep='last', subset=['player_id', 'champion', 'kill_', 'death', 'assist', 'position', 'is_win'])

    # Create two new columns win and lose to give the information of the outcome of the finished games
    df['win'] = df['is_win'].apply(lambda x: 1 if x else 0)
    df['lose'] = df['is_win'].apply(lambda x: 1 if not x else 0)
    df.drop(columns=['is_win'], inplace=True)

    df.dropna(inplace=True)

    return df

def load_recent_games_data(name, df)-> None:

    filame = f"recent_games_data_{name}.csv"
    try:
        df.to_csv(filame, sep=',', index=False)
        logging.info(f"csv data saved to {filame}")
    except Exception as err:
        logging.error(f"Error saving data to csv: {err}")
    
    return None

def ETL_pipeline_recent_games_data()-> None:

    champion_data = extract_recent_games_data(id)
    df =transform_recent_games_data(champion_data)
    load_recent_games_data(name, df)

    return None

if __name__ == "__main__":

    id, name = insert_name("souvenir13")

    ETL_pipeline_champions_data()
    ETL_pipeline_season_data()
    ETL_pipeline_summoner_data()
    ETL_pipeline_season_history_data()
    ETL_pipeline_recent_games_data()



    


