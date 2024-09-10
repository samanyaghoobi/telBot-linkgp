
import json
#######################
SETTINGS_FILE_NAME = "settings.json"
defaultSetting = {
    "testMode": False,
    "disable_notification": True,
    "sendBannerNotification": False,
    "restart_msg": True,
}
#######################
def save_settings(settings):
    with open(SETTINGS_FILE_NAME, 'w') as f:
        json.dump(settings, f)

#######################
def load_settings():
    try:
        with open(SETTINGS_FILE_NAME, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        save_settings(defaultSetting)
        return defaultSetting
