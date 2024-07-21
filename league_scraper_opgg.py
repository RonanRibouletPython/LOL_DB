from opgg.opgg import OPGG
from opgg.params import Region

import json
from typing import Dict
import logging

from utils import extract_summoner_data

from logging_setup import setup_logging

# Logging setup
setup_logging(log_file="logs/league_scraper_opgg.log", level=logging.DEBUG)

# Parameters
summoner_name = "souvenir#2310"  
region = Region.EUW


def save_to_json(data: Dict, filename: str = f"summoner_data_{summoner_name}.json"):
    """Saves the given data to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving data to JSON: {e}")



def run_fetching(summoner_name: str, region: Region):
    """Main function to fetch, process, and save summoner data."""
    opgg = OPGG()
    summoner = opgg.search(summoner_name, region)
    
    # Adding the region to the JSON file 
    temp = {
        "region" : region
    }

    if summoner:
        try: 
            summoner_data = extract_summoner_data(summoner)
            summoner_data.update(temp)
            save_to_json(summoner_data)

            logging.debug(f"Summoner data for {summoner_name} saved to summoner_data.json")
        except Exception as e:
            logging.debug(f"Summoner {summoner_name} not found throwing error: {e}")

if __name__ == "__main__":
    run_fetching(summoner_name, region)