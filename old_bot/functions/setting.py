
from datetime import datetime
import json
import logging
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
#######################
def init_logger():
        #log init
        log_filename = f"./logs/output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        
        logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        logging.info("bot is Started")
