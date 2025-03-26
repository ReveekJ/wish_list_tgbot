import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_AIOGRAM_DB = int(os.environ.get('REDIS_AIOGRAM_DB'))
REDIS_TASKIQ_DB = int(os.environ.get('REDIS_TASKIQ_DB'))
REDIS_USER_SCHEDULES_DB = int(os.environ.get('REDIS_USER_SCHEDULES_DB'))

NATS_HOST = os.environ.get('NATS_HOST')
NATS_PORT = os.environ.get('NATS_PORT')

TOKEN = os.environ.get('TOKEN')
LINK_FOR_BOT = os.environ.get('LINK_FOR_BOT')
PATH_TO_WISH_IMAGES = os.environ.get('PATH_TO_WISH_IMAGES')

CACHE_USER_DB = int(os.environ.get('CACHE_USER_DB'))
CACHE_WISH_LIST_DB = int(os.environ.get('CACHE_WISH_LIST_DB'))
CACHE_WISH_DB = int(os.environ.get('CACHE_WISH_DB'))
CACHE_WISH_LIST_MEMBERS_SECONDARY_DB = int(os.environ.get('CACHE_WISH_LIST_MEMBERS_SECONDARY_DB'))
CACHE_LAST_MESSAGE_ID = int(os.environ.get('CACHE_LAST_MESSAGE_ID'))
REDIS_SECURITY_CODE_DB = int(os.environ.get('REDIS_SECURITY_CODE_DB'))
