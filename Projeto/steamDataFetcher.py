import os
import pickle
from steam_web_api import Steam
import requests
import random
import json

#os.system('chcp 65001')
KEY = os.environ.get("134FB76FD1295AF1BCCA484FED9947E5")
steam = Steam(KEY)
appId1 = '2766090' #random funcciona
appId2 = '1088710' #yakuza
appId3 = '609970' #random não funcciona
appId4 = '1435010'
cache_file = 'cache/game-details-cache.json'

# Load cache from file if it exists
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        cache = json.load(f)
else:
    cache = {1: {}}


def get_random_appids(num_items):
    print('before')
    results = random.sample(get_all_appids(), num_items)
    results = [str(appid) for appid in results]  # Convert app IDs to strings
    print(results)
    print('after')
    return results


def get_all_appids():
    response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    data = response.json()
    all_appids = []  # Initialize list to store all app ids
    for app in data['applist']['apps']: 
        if app.get('name'):
            all_appids.append(app['appid'])  # Add each app id to the list
    return all_appids

"""
def get_game_details(app_id):
    # Try to get data from cache first
    game_details = cache.get(app_id)
    if game_details is not None:
        print('cached \n\n\n',game_details, "\n\n\n --------------------------------------------------\n\n")
        return game_details

    # If data is not in cache, fetch it from the API
    details = steam.apps.get_app_details(app_id,country ='US', filters="basic,screenshots")
    game_details = details.get(app_id, {}).get('data', {})

    # Store data in cache
    cache[app_id] = game_details

    # Save cache to file
    with open(cache_file, 'wb') as f:
        pickle.dump(cache, f)
    print('not cached \n\n\n',game_details, "\n\n\n --------------------------------------------------\n\n")
    return game_details


"""
def cache_game_details(app_id, game_details):
    # Cache the data
    cache[app_id] = game_details
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f)


def get_game_details(app_id):
    # Try to get data from cache first
    game_details = cache.get(app_id)
    if game_details is not None:
        print(('cached       ' + json.dumps(game_details, ensure_ascii=False) + '---------------------------------------------------------------------------------------------------------------------').encode('utf-8'))
        return game_details

    # If data is not in cache, fetch it from the API
    details = steam.apps.get_app_details(app_id,country ='US', filters="basic,screenshots")
    game_details = details.get(app_id, {}).get('data', {})

    # Check if game details are empty
    if not game_details:
        print("nothing found")
        return

    # Call the new function to cache the data autoomatically
    #cache_game_details(app_id, game_details)

    print(('fetched       ' + json.dumps(game_details, ensure_ascii=False) + '---------------------------------------------------------------------------------------------------------------------').encode('utf-8'))
    return game_details

def is_cached(app_id):
    
    result = app_id in cache
    print(result)
    return result

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



#get_game_details(appId4)
#print(get_screenshots(appId1,5))
#print(get_random_appids(1)[0])
#print(get_random_appids(1)[0])
#get_game_details(get_random_appids(1)[0])
#get_game_details(get_random_appids(1)[0])
cache_game_details(appId1, get_game_details(appId1))
#get_all_appids()
#is_cached(appId1)
