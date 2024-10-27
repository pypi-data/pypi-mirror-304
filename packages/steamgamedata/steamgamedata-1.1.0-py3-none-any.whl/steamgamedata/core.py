import requests
import json

def pull(appid):
    """
    Fetches game data from the Steam API using the provided app ID.

    Args:
        appid (int): The app ID of the game.

    Returns:
        dict or None: Game data if successful, None otherwise.
    """
    url = f"http://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    data = response.json()

    if str(appid) in data and data[str(appid)]['success']:
        return data[str(appid)]
    else:
        print(f"Error: Data for appid {appid} not found or API call failed.")
        return None  # Return None if there's no valid data

def write(filename, data):
    """
    Writes the fetched game data to a JSON file.

    Args:
        filename (str): The name of the file to save the data.
        data (dict): The game data to be saved.
    """
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)  # Pretty print with 4 spaces of indentation
    print(f"Game data has been written to {filename}.")

def save_data(appid, filename):
    """
    Fetches game data and saves it to a specified file.

    Args:
        appid (int): The app ID of the game.
        filename (str): The name of the file to save the data.
    """
    data = pull(appid)
    if data is None:
        print(f"Failed to fetch data for appid {appid}.")
        return

    write(filename, data)
