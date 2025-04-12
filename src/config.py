"""
Конфиг бота
"""

from os import path, getenv

import dotenv


# Program state & config
STATE_PATH = path.join(path.dirname(__file__), "../state")

dotenv.load_dotenv(path.join(STATE_PATH, ".env"))

# Mail
PASSWORD = getenv("TGRS_PASSWORD")
USERNAME = getenv("TGRS_USERNAME")
IMAP_SERVER = getenv("TGRS_IMAP_SERVER")
DEFAULT_INBOX = getenv("TGRS_DEFAULT_INBOX")
LISTEN_DELAY = int(getenv("TGRS_LISTEN_DELAY"))

# Telegram
TELEGRAM_TOKEN = getenv("TGRS_TOKEN")
