import pytz
from peewee import *

db = SqliteDatabase('db/backend.db')

timezone = pytz.timezone("America/Los_Angeles")
