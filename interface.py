from db_data_adder import (insert_data_summoners_table,
                           insert_data_season_history_table,
                           insert_data_league_stats_table,
                           insert_data_champion_stats_table,
                           insert_data_recent_games_table
                        )
from league_scraper_opgg import run_fetching

from ETL_pipeline_champions_data import (insert_name,
                                         ETL_pipeline_champions_data,
                                         ETL_pipeline_season_data,
                                         ETL_pipeline_summoner_data,
                                         ETL_pipeline_season_history_data,
                                         ETL_pipeline_recent_games_data
                                    )

from logging_setup import setup_logging

from opgg.params import Region
import os
import shutil

import logging
# Logging setup
setup_logging(log_file="logs/interface.log", level=logging.DEBUG)

def UI():
    
    print("\nWelcome to the League of Legends Database Pipeline interface!")

    region_map = {
        'NA': Region.NA,
        'EUW': Region.EUW,
        'LAN': Region.LAN,
        'LAS': Region.LAS,
        'OCE': Region.OCE,
        'RU': Region.RU,
        'BR': Region.BR,
        'TR': Region.TR,
    }

    summoner_name = input("Enter the summoner name: ")
    region = input("Enter the region (NA, EUW, LAN, LAS, OCE, RU, BR, TR): ")

    summoner_name_without_tag = summoner_name.split("#")[0]

    dirname = f"files_{summoner_name_without_tag}"
    try:
        os.makedirs(dirname, exist_ok=True)
    except Exception as e:
        logging.error(f"Error creating directory: {e}")
        
    if region.lower() in ['na', 'euw', 'lan', 'las', 'oce', 'ru', 'br', 'tr']:
        region_obj = region_map[region.upper()]

        logging.info(f"Running fetching for summoner {summoner_name} in region {region}")
        file_path = run_fetching(summoner_name, region_obj)

    id, name = insert_name(summoner_name_without_tag)


    insert_data_summoners_table(file_path)
    insert_data_season_history_table(file_path)
    insert_data_league_stats_table(file_path)
    insert_data_champion_stats_table(file_path)
    insert_data_recent_games_table(file_path)

    ETL_pipeline_champions_data(id, name)

    ETL_pipeline_season_data(id, name)

    ETL_pipeline_summoner_data(id, name)

    ETL_pipeline_season_history_data(id, name)

    ETL_pipeline_recent_games_data(id, name)

    # Store the csv files of the summoner under dirname/csv + delete the json file
    
    os.remove(file_path)
    logging.info(f"Json file {os.path.basename(file_path)} deleted")
    os.makedirs(f"{dirname}/csv", exist_ok=True)

    shutil.move(f"recent_games_data_{summoner_name_without_tag}.csv", f"{dirname}/csv")
    shutil.move(f"season_data_{summoner_name_without_tag}.csv", f"{dirname}/csv")
    shutil.move(f"season_history_data_{summoner_name_without_tag}.csv", f"{dirname}/csv")
    shutil.move(f"summoner_data_{summoner_name_without_tag}.csv", f"{dirname}/csv")
    shutil.move(f"champions_data_{summoner_name_without_tag}.csv", f"{dirname}/csv")  
    logging.info(f"csv files store to {dirname}/csv")

    logging.info(f"Data pipeline completed for summoner {summoner_name} in region {region}")
    logging.info(f"The csv files can be used in a data analysis software !")

if __name__ == "__main__":
    UI()