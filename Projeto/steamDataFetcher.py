import os
from steam_web_api import Steam

KEY = os.environ.get("134FB76FD1295AF1BCCA484FED9947E5")
steam = Steam(KEY)

appId = '1088710'

def get_screenshots(app_id, num_screenshots):
    details = steam.apps.get_app_details(app_id, filters="screenshots")
    screenshots = details.get(app_id, {}).get('data', {}).get('screenshots', [])
    return [screenshot['path_thumbnail'] for screenshot in screenshots[:num_screenshots]]


screenshots = get_screenshots(appId,5)
for screenshot in screenshots:
    print(screenshot)