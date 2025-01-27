import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
TOKEN = os.environ.get('TOKEN')
LINK_FOR_BOT = os.environ.get('LINK_FOR_BOT')
PATH_TO_WISH_IMAGES = os.environ.get('PATH_TO_WISH_IMAGES')
