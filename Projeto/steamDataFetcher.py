import os
import pickle
from steam_web_api import Steam
import requests
import random

KEY = os.environ.get("134FB76FD1295AF1BCCA484FED9947E5")
steam = Steam(KEY)
appId1 = '2766090'
appId2 = '1088710'
cache_file = 'cache/game-details-cache.pkl'

# Load cache from file if it exists
if os.path.exists(cache_file):
    with open(cache_file, 'rb') as f:
        cache = pickle.load(f)
else:
    cache = {}


def get_random_appids(array, num_items):
    return random.sample(array, num_items)


def get_all_appids(): #retorna array com todos os id s possiveis para escolher randoms
    response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    data = response.json()
    all_appids = [app['appid'] for app in data['applist']['apps']]
    return all_appids

def get_game_details(app_id):
    # Try to get data from cache first
    game_details = cache.get(app_id)
    if game_details is not None:
        print("cached \n \n", game_details,"\n\n\n --------------------------------------------------\n\n")
        return game_details

    # If data is not in cache, fetch it from the API
    details = steam.apps.get_app_details(app_id, filters="basic,screenshots")
    game_details = details.get(app_id, {}).get('data', {})

    # Store data in cache
    cache[app_id] = game_details

    # Save cache to file
    with open(cache_file, 'wb') as f:
        pickle.dump(cache, f)
    print("not cached \n \n",game_details,"\n\n\n --------------------------------------------------\n\n")
    return game_details


def get_type(app_id):
    return get_game_details(app_id).get('type')

def get_name(app_id):
    return get_game_details(app_id).get('name')

def get_steam_appid(app_id):
    return get_game_details(app_id).get('steam_appid')

def get_required_age(app_id):
    return get_game_details(app_id).get('required_age')

def get_is_free(app_id):
    return get_game_details(app_id).get('is_free')

def get_detailed_description(app_id):
    return get_game_details(app_id).get('detailed_description')

def get_about_the_game(app_id):
    return get_game_details(app_id).get('about_the_game')

def get_short_description(app_id):
    return get_game_details(app_id).get('short_description')

def get_supported_languages(app_id):
    return get_game_details(app_id).get('supported_languages')

def get_header_image(app_id):
    return get_game_details(app_id).get('header_image')

def get_capsule_image(app_id):
    return get_game_details(app_id).get('capsule_image')

def get_capsule_imagev5(app_id):
    return get_game_details(app_id).get('capsule_imagev5')

def get_website(app_id):
    return get_game_details(app_id).get('website')

def get_pc_requirements(app_id):
    return get_game_details(app_id).get('pc_requirements')

def get_mac_requirements(app_id):
    return get_game_details(app_id).get('mac_requirements')

def get_linux_requirements(app_id):
    return get_game_details(app_id).get('linux_requirements')

def get_legal_notice(app_id):
    return get_game_details(app_id).get('legal_notice')


def get_screenshots(app_id, n):
    # Get game details
    game_details = get_game_details(app_id)

    # Get screenshots
    screenshots = game_details.get('screenshots', [])

    # Get paths of first n screenshots
    screenshot_paths = [screenshot['path_thumbnail'] for screenshot in screenshots[:n]]

    return screenshot_paths


#print(get_screenshots(appId,5))
#get_game_details(appId2)
print(get_screenshots(appId1,5))
