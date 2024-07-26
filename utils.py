
from opgg.summoner import Summoner

from typing import Dict
from datetime import datetime

import requests # request img from web
import shutil # save img locally

def img_download_from_url(url: str, filename: str) -> None:
    """Download an image from a URL and save it locally."""
    response = requests.get(url, stream=True)
    response.raise_for_status()

def extract_summoner_data(summoner: Summoner) -> Dict:
    """Extracts relevant data from a Summoner object into a dictionary."""

    base_year = datetime.now().year

    return {
        "id": summoner.id,
        "summoner_id": summoner.summoner_id,
        "account_id": summoner.acct_id,
        "puuid": summoner.puuid,
        "game_name": summoner.game_name,
        "tagline": summoner.tagline,
        "name": summoner.name,
        "internal_name": summoner.internal_name,
        "profile_image_url": summoner.profile_image_url,
        "level": summoner.level,
        "updated_at": str(summoner.updated_at),
        "renewable_at": str(summoner.renewable_at),
        "previous_seasons": [
            {
                "season": base_year - index, 
                "tier": seasons.tier_info.tier, 
                "division": seasons.tier_info.division, 
                "lp": seasons.tier_info.lp} 
            for index, seasons in enumerate(summoner.previous_seasons)
        ],
        "league_stats": [
            {
                "queue_type": stat.queue_info.game_type, 
                "tier": stat.tier_info.tier, 
                "division": stat.tier_info.division, 
                "lp": stat.tier_info.lp, 
                "win": stat.win, 
                "lose": stat.lose, 
                "winrate": stat.win_rate}
            for stat in summoner.league_stats
        ],
        "most_champions": [
            {
                "champion": champ.champion.name, 
                "win": champ.win, 
                "lose": champ.lose, 
                "winrate": champ.win_rate, 
                "kda": champ.kda}
            for champ in summoner.most_champions
        ],
        "recent_game_stats": [
            {
                "champion": game.champion.name, 
                "kill": game.kill, 
                "death": game.death, 
                "assist": game.assist, 
                "position": game.position, 
                "is_win": game.is_win}
            for game in summoner.recent_game_stats
        ],
    }
