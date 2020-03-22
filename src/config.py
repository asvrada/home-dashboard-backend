import pytz
import logging
from peewee import *

# Setting/Configuration

DEBUG = True

DB_PATH = "db/backend.db"
LOG_PATH = "app.log"
LOG_LEVEL_PROD = logging.INFO
TIMEZONE = "America/Los_Angeles"

# "Global" variable
if DEBUG:
    logging.basicConfig(level=LOG_LEVEL_PROD)
else:
    # Production logging
    logging.basicConfig(filename=LOG_PATH, level=LOG_LEVEL_PROD)

db = SqliteDatabase(DB_PATH)

timezone = pytz.timezone(TIMEZONE)
