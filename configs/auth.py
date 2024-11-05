from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

##############################################################
CHANNELS_USERNAME=['@linkGP']
SUPPORT_USERNAME='@linkgp_admin'
SUPPORT_ID=340500740
ADMIN_ID_LIST=[1054820423,340500740]
BOT_USERNAME="linkgp_adminBot"