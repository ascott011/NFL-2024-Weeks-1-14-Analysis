import json
import glob
import os

# Create a list to store all data
all_games = []

# Read all JSON files from the boxscores directory
files = glob.glob('2024-nfl-boxscores/*.json')

for file in files:
    with open(file, 'r') as f:
        data = json.load(f)
        # Extract game_id from filename
        game_id = file.split('game_')[1].replace('.json', '')
        
        # Add game_id to the data
        data['game_id'] = game_id
        all_games.append(data)

# Save combined data
with open('2024-nfl-boxscores/weeks1-14_2024_nfl_boxscores.json', 'w') as f:
    json.dump(all_games, f, indent=2)

print(f"Combined {len(files)} games into weeks1-14_2024_nfl_boxscores.json")
