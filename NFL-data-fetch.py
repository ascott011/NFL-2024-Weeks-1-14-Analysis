import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('SPORTRADAR_API_KEY')
# First, get the schedule to get all game IDs
schedule_url = "https://api.sportradar.com/nfl/official/trial/v7/en/games/2024/REG/schedule.json"

# Create directory if it doesn't exist
os.makedirs('2024-nfl-boxscores', exist_ok=True)

response = requests.get(schedule_url, params={'api_key': API_KEY})
if response.status_code == 200:
    schedule = response.json()
    games = schedule.get('weeks', [])
    
    for week in games:
        for game in week.get('games', []):
            game_id = game.get('id')
            
            # Check if we already have this game's data
            file_name = f"2024-nfl-boxscores/game_{game_id}.json"
            if os.path.exists(file_name):
                print(f"Already have data for game {game_id}")
                continue
                
            boxscore_url = f"https://api.sportradar.com/nfl/official/trial/v7/en/games/{game_id}/boxscore.json"
            
            try:
                response = requests.get(boxscore_url, params={'api_key': API_KEY})
                if response.status_code == 200:
                    data = response.json()
                    with open(file_name, 'w') as f:
                        json.dump(data, f, indent=2)
                    print(f"Saved boxscore for game {game_id}")
                else:
                    print(f"Failed to get boxscore for game {game_id}: {response.status_code}")
                
                # Respect API rate limits
                time.sleep(1.2)
                
            except Exception as e:
                print(f"Error fetching game {game_id}: {e}")
else:
    print(f"Failed to get schedule: {response.status_code}")