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

# Construct query for the MySQL DB for the Summoners table
def insert_data_summoners_table(file_path: str)-> str:

    summoners_data = extract_summoners_data_from_json(file_path)

    cursor = lol_db.cursor()

    # Construct the query
    query = """
        INSERT INTO Summoners (
            opgg_id,
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
        VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

# Extract the JSON data for the Season_History table of the DB
def extract_season_history_data_from_json(file_path: str) -> dict: 
    # Open the JSON file
    try:
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
            logging.info("JSON file opened successfully.")
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {file_path}")
        raise
    
    # Extract the previous seasons data from the JSON file
    previous_seasons = json_data["previous_seasons"]

    # Create a list to store the tuples
    info_queries: list[tuple[str, str, str, str, str]] = []

    try:
        for season in previous_seasons:

            info_query: tuple[str, str, str, str, str] = (
                json_data['id'],
                season["season"],
                season["tier"],
                season["division"],
                season['lp'], 
            )
            info_queries.append(info_query) 
            logging.info(f"append data from the season {season["season"]} to the list of tuples")          
    except KeyError:
        logging.error(f"Unable to append the JSON data to the list.")
        raise

    return info_queries

# Construct query for the MySQL DB for the Season_History table
def insert_data_season_history_table(file_path: str)-> str:

    list_seasons_history = extract_season_history_data_from_json(file_path)

    cursor = lol_db.cursor()

    # Construct the query
    query = """
        INSERT INTO Season_History (
            player_id,
            season,
            tier,
            division,
            lp
            )
        VALUES (%s, %s, %s, %s, %s)
    """
    for seasons_history in list_seasons_history:
        # Execute the query
        try:
            cursor.execute(query, seasons_history)
            lol_db.commit()
            logging.info("Data inserted into Summoners table successfully.")
        except sql.Error as err:
            logging.error(f"Error inserting data into Summoners table: {err}")
            lol_db.rollback()

    return(cursor.rowcount, "record inserted.")

# Extract the JSON data for the League_Stats table of the DB
def extract_season_league_stats_from_json(file_path: str) -> dict: 
    # Open the JSON file
    try:
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
            logging.info("JSON file opened successfully.")
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {file_path}")
        raise
    
    # Extract the previous seasons data from the JSON file
    queues = json_data["league_stats"]

    # Create a list to store the tuples
    info_queries: list[tuple[str, str, str, str, str, str, str, float]] = []

    try:
        for queue in queues:

            info_query: tuple[str, str, str, str, str, str, str, float] = (
                json_data['id'],
                queue["queue_type"],
                queue["tier"],
                queue["division"],
                queue['lp'],
                queue['win'],
                queue['lose'],
                queue['winrate'],
            )

            info_queries.append(info_query) 
            logging.info(f"append data from the queue type {queue["queue_type"]} to the list of tuples")          
    except KeyError:
        logging.error(f"Unable to append the JSON data to the list.")
        raise

    return info_queries

# Construct query for the MySQL DB for the League_Stats table
def insert_data_league_stats_table(file_path: str)-> str:

    list_league_stats = extract_season_league_stats_from_json(file_path)

    cursor = lol_db.cursor()

    # Construct the query
    query = """
        INSERT INTO League_Stats (
            player_id,
            queue_type,
            tier,
            division,
            lp,
            win,
            lose,
            winrate
            )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    for league_stats in list_league_stats:
        # Execute the query
        try:
            cursor.execute(query, league_stats)
            lol_db.commit()
            logging.info("Data inserted into Summoners table successfully.")
        except sql.Error as err:
            logging.error(f"Error inserting data into Summoners table: {err}")
            lol_db.rollback()

    return(cursor.rowcount, "record inserted.")

# Extract the JSON data for the Champion_Stats table of the DB
def extract_season_champion_stats_from_json(file_path: str) -> dict: 
    # Open the JSON file
    try:
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
            logging.info("JSON file opened successfully.")
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {file_path}")
        raise
    
    # Extract the previous seasons data from the JSON file
    champions = json_data["most_champions"]

    # Create a list to store the tuples
    info_queries: list[tuple[str, str, str, str, float, float]] = []

    try:
        for champion in champions:

            info_query: tuple[str, str, str, str, float, float] = (
                json_data['id'],
                champion["champion"],
                champion["win"],
                champion["lose"],
                champion['winrate'],
                champion['kda'],
            )

            info_queries.append(info_query) 
            logging.info(f"append data with statistics with the champion {champion["champion"]} to the list of tuples")          
    except KeyError:
        logging.error(f"Unable to append the JSON data to the list.")
        raise

    return info_queries

# Construct query for the MySQL DB for the Champion_Stats table
def insert_data_champion_stats_table(file_path: str)-> str:

    list_champions_played = extract_season_champion_stats_from_json(file_path)

    cursor = lol_db.cursor()

    # Construct the query
    query = """
        INSERT INTO Champion_Stats (
            player_id,
            champion,
            win,
            lose,
            winrate,
            kda
            )
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    for champions_played in list_champions_played:
        # Execute the query
        try:
            cursor.execute(query, champions_played)
            lol_db.commit()
            logging.info("Data inserted into Summoners table successfully.")
        except sql.Error as err:
            logging.error(f"Error inserting data into Summoners table: {err}")
            lol_db.rollback()

    return(cursor.rowcount, "record inserted.")

# Extract the JSON data for the Recent_Games table of the DB
def extract_season_recent_games_from_json(file_path: str) -> dict: 
    # Open the JSON file
    try:
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
            logging.info("JSON file opened successfully.")
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        raise
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in file: {file_path}")
        raise
    
    # Extract the previous seasons data from the JSON file
    recent_game_stats = json_data["recent_game_stats"]

    # Create a list to store the tuples
    info_queries: list[tuple[str, str, int, int, int, str, bool]] = []

    try:
        for recent_game_stat in recent_game_stats:

            info_query: tuple[str, str, int, int, int, str, bool] = (
                json_data['id'],
                recent_game_stat["champion"],
                recent_game_stat["kill"],
                recent_game_stat["death"],
                recent_game_stat['assist'],
                recent_game_stat['position'],
                recent_game_stat['is_win'],
            )

            info_queries.append(info_query) 
            logging.info(f"append data from the recent game played with {recent_game_stat["champion"]} to the list of tuples")          
    except KeyError:
        logging.error(f"Unable to append the JSON data to the list.")
        raise

    return info_queries

# Construct query for the MySQL DB for the Recent_Games table
def insert_data_recent_games_table(file_path: str)-> str:

    list_recent_games = extract_season_recent_games_from_json(file_path)

    cursor = lol_db.cursor()

    # Construct the query
    query = """
        INSERT INTO Recent_Game_Stats (
            player_id,
            champion,
            kill_,
            death,
            assist,
            position,
            is_win
            )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    for recent_games in list_recent_games:
        # Execute the query
        try:
            cursor.execute(query, recent_games)
            lol_db.commit()
            logging.info("Data inserted into Summoners table successfully.")
        except sql.Error as err:
            logging.error(f"Error inserting data into Summoners table: {err}")
            lol_db.rollback()

    return(cursor.rowcount, "record inserted.")

if __name__ == "__main__":
    file_path = "summoner_data_Eragon#6027.json"
    insert_data_summoners_table(file_path)
    insert_data_season_history_table(file_path=file_path)
    insert_data_league_stats_table(file_path)
    insert_data_champion_stats_table(file_path)
    insert_data_recent_games_table(file_path)