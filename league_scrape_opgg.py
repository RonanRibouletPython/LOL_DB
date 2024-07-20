from opgg.opgg import OPGG
from opgg.params import Region

import json
from typing import Dict

from utils import extract_summoner_data as ext

# Parameters
summoner_name = "souvenir#2310"  
region = Region.EUW


def save_to_json(data: Dict, filename: str = f"summoner_data_{summoner_name}.json"):
    """Saves the given data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def run_fetching(summoner_name: str, region: Region):
    """Main function to fetch, process, and save summoner data."""
    opgg = OPGG()
    summoner = opgg.search(summoner_name, region)
    
    if summoner:
        summoner_data = ext(summoner)
        save_to_json(summoner_data)
        print(f"Summoner data for {summoner_name} saved to summoner_data.json")
    else:
        print(f"Summoner {summoner_name} not found.")


if __name__ == "__main__":
    run_fetching(summoner_name, region)