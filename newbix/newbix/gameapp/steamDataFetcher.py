import os
import pickle
from steam_web_api import Steam
import requests
import random
import json

os.system('chcp 65001')
KEY = os.environ.get("134FB76FD1295AF1BCCA484FED9947E5")
steam = Steam(KEY)
appId1 = '2766090'  # random funcciona
appId2 = '1088710'  # yakuza
appId3 = '609970'  # random não funcciona
appId4 = '1435010'
cache_file = 'gameapp/static/cache/game-details-cache.json'

# Load cache from file if it exists
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        if f.read():
            f.seek(0)  # Reset file read position
            cache = json.load(f)
        else:
            cache = {}
else:
    cache = {1: {}}


def get_random_appids(num_items):

    results = random.sample(get_all_appids(), num_items)
    results = [str(appid) for appid in results]  # Convert app IDs to strings

    return results

def get_random_games(num_games):
    games = []
    while len(games) < num_games:
        app_id = get_random_appids(1)[0]
        game_details = get_game_details(app_id)
        if game_details is not None and game_details.get('type') == 'game':
            games.append(game_details)
    return games

def get_all_appids():
    response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    data = response.json()
    all_appids = []  # Initialize list to store all app ids
    for app in data['applist']['apps']:
        if app.get('name'):
            all_appids.append(app['appid'])  # Add each app id to the list
    return all_appids


def cache_game_details(app_id):
    # Cache the data
    if is_cached(app_id):
        print('already cached')
        return
    print(os.getcwd())
    cache[app_id] = get_game_details(app_id)
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f)
    print('cached')


def remove_from_cache(app_id):
    if app_id in cache:
        del cache[app_id]
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f)
        print('removed from cache')
        return
    print('not in cache')


def get_game_details(app_id):
    # Try to get data from cache first
    app_id = str(app_id)
    game_details = cache.get(app_id)
    if game_details is not None:
        # print(('cached       ' + json.dumps(game_details, ensure_ascii=False) + '---------------------------------------------------------------------------------------------------------------------').encode('utf-8'))
        return game_details

    # If data is not in cache, fetch it from the API
    details = steam.apps.get_app_details(app_id, filters="basic,screenshots")
    game_details = details.get(app_id, {}).get('data', {})

    # Check if game details are empty
    if not game_details:
        print("nothing found")
        return

    # Call the new function to cache the data autoomatically
    # cache_game_details(app_id, game_details)

    # print(('fetched       ' + json.dumps(game_details, ensure_ascii=False) + '---------------------------------------------------------------------------------------------------------------------').encode('utf-8'))
    return game_details


def is_cached(app_id):
    result = app_id in cache
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


def get_search_results_array(keyword):
    keyword = str(keyword)  # Convert keyword to string
    result = steam.apps.search_games(keyword)
    # print(result)
    return result['apps']


def get_screenshots(app_id):
    game_details = get_game_details(app_id)

    # Get screenshots
    screenshots = game_details.get('screenshots', [])
    return screenshots


def get_background(app_id):
    sShots = get_screenshots(app_id)
    background = None
    if sShots:
        background = random.choice(sShots)
    return background


def get_header_img(app_id):
    game_details = get_game_details(app_id)
    return parse_header_image(game_details)


def parse_type(game_details):
    return game_details.get('type')


def parse_name(game_details):
    return game_details.get('name')


def parse_steam_appid(game_details):
    return game_details.get('steam_appid')


def parse_required_age(game_details):
    return game_details.get('required_age')


def parse_is_free(game_details):
    return game_details.get('is_free')


def parse_detailed_description(game_details):
    return game_details.get('detailed_description')


def parse_about_the_game(game_details):
    return game_details.get('about_the_game')


def parse_short_description(game_details):
    return game_details.get('short_description')


def parse_supported_languages(game_details):
    return game_details.get('supported_languages')


def parse_header_image(game_details):
    return game_details.get('header_image')


def parse_capsule_image(game_details):
    return game_details.get('capsule_image')


def parse_capsule_imagev5(game_details):
    return game_details.get('capsule_imagev5')


def parse_website(game_details):
    return game_details.get('website')


def parse_pc_requirements(game_details):
    return game_details.get('pc_requirements')


def parse_mac_requirements(game_details):
    return game_details.get('mac_requirements')


def parse_linux_requirements(game_details):
    return game_details.get('linux_requirements')


def parse_legal_notice(game_details):
    return game_details.get('legal_notice')


def parse_screenshots(game_details, n):
    # Get screenshots
    screenshots = game_details.get('screenshots', [])

    # Get paths of first n screenshots
    screenshot_paths = [screenshot['path_thumbnail'] for screenshot in screenshots[:n]]

    return screenshot_paths


def parse_result_id(game):
    return game.get('id')


def parse_result_link(game):
    return game.get('link')


def parse_result_name(game):
    return game.get('name')


def parse_result_img(game):
    return game.get('img')


def parse_result_price(game):
    return game.get('price')

# print(parse_result_img(get_search_results_array('yakuza')[0]))
# get_game_details(appId3)
# print(is_cached(appId1))
# cache_game_details(appId1)
# print(is_cached(appId1))
# remove_from_cache(appId1)
# print(is_cached(appId1))
# print(get_screenshots(appId2,5))
# print(get_random_appids(1)[0])
# print(get_random_appids(1)[0])
# get_game_details(get_random_appids(1)[0])
# get_game_details(get_random_appids(1)[0])
# get_all_appids()
